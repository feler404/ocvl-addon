"""
*n_requirements:*
Default requirements
    - "__and__": ["src_in", "dst_in"]
Alternative requirements
    - "__or__": ["layer_0_in", "layer_1_in", "image_2_in"]

*n_quick_link_requirements:*
Default node for Image/Matrix Socket
    - "src_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
Override node type
    - "m_in": {"__type_node__": "OCVLMatNode", "loc_input_mode": "MANUAL", "loc_manual_input": "[[0, 1], [2, 10]]"}
"""
from collections import defaultdict
from copy import deepcopy

import bpy
from ocvl.core import settings
from ocvl.core import globals as ocvl_globals
from ocvl.core.exceptions import LackRequiredSocketException
from ocvl.core.globals import SOCKET_DATA_CACHE
from ocvl.core.register_utils import ocvl_register, ocvl_unregister


sentinel = object()


def get_socket_id(socket):
    return str(hash(socket.id_data.name + socket.node.name + socket.identifier))


def process_from_socket(self, context):
    """Update function of exposed properties in Sockets"""
    self.node.process_node(context)


def get_other_socket(socket):
    """
    Get next real upstream socket.
    This should be expanded to support wifi nodes also.
    Will return None if there isn't a another socket connect
    so no need to check socket.links
    """
    if not socket.is_linked or not socket.links:
        return None
    if socket.is_output:
        other = socket.links[0].to_socket
    else:
        other = socket.links[0].from_socket

    if other.node.bl_idname == 'NodeReroute':
        if not socket.is_output:
            return get_other_socket(other.node.inputs[0])
        else:
            return get_other_socket(other.node.outputs[0])
    else:  #other.node.bl_idname == 'WifiInputNode':
        return other


def set_socket(socket, out):
    """sets socket data for socket"""
    # if data_structure.DEBUG_MODE:
    #     if not socket.is_output:
    #         warning("{} setting input socket: {}".format(socket.node.name, socket.name))
    #     if not socket.is_linked:
    #         warning("{} setting unconncted socket: {}".format(socket.node.name, socket.name))
    s_id = socket.socket_id
    s_ng = socket.id_data.name
    if s_ng not in SOCKET_DATA_CACHE:
        SOCKET_DATA_CACHE[s_ng] = {}
    SOCKET_DATA_CACHE[s_ng][s_id] = out


def get_socket(socket, deepcopy_=True):
    """gets socket data from socket,
    if deep copy is True a deep copy is make_dep_dict,
    to increase performance if the node doesn't mutate input
    set to False and increase performance substanstilly
    """
    if socket.is_linked:
        other = socket.other
        if other:
            s_id = other.socket_id
            s_ng = other.id_data.name
            if s_ng not in SOCKET_DATA_CACHE:
                if not ocvl_globals.MUTE_LOOKUP_ERROR:
                    raise LookupError
                else:
                    raise LackRequiredSocketException(socket)
            if s_id in SOCKET_DATA_CACHE[s_ng]:
                out = SOCKET_DATA_CACHE[s_ng][s_id]
                if deepcopy_:
                    return deepcopy(out)
                else:
                    return out
            else:
                # if data_structure.DEBUG_MODE:
                #     debug("cache miss: %s -> %s from: %s -> %s",
                #             socket.node.name, socket.name, other.node.name, other.name)
                raise LackRequiredSocketException(socket)
    # not linked
    raise LackRequiredSocketException(socket)


def get_socket_info(socket):
    """returns string to show in socket label"""
    ng = socket.id_data.name

    if socket.is_output:
        s_id = socket.socket_id
    elif socket.is_linked:
        other = socket.other
        if other:
            s_id = other.socket_id
        else:
            return ''
    else:
        return ''
    if ng in SOCKET_DATA_CACHE:
        if s_id in SOCKET_DATA_CACHE[ng]:
            data = SOCKET_DATA_CACHE[ng][s_id]
            if data:
                return str(len(data))
    return ''


def recursive_framed_location_finder(node, loc_xy):
    locx, locy = loc_xy
    if node.parent:
        locx += node.parent.location.x
        locy += node.parent.location.y
        return recursive_framed_location_finder(node.parent, (locx, locy))
    else:
        return locx, locy


def get_new_input_node_idname(node, socket):
    if socket.bl_idname == "OCVLImageSocket":
        new_node_idname = node.n_quick_link_requirements.get(node.inputs[socket.index].name, {}).get("__type_node__",
                                                                                                   settings.DEFAULT_NODE_FOR_QUICK_LINK_IMAGE_SOCKET)
    elif socket.bl_idname == "OCVLMaskSocket":
        new_node_idname = settings.DEFAULT_NODE_FOR_QUICK_LINK_MASK_SOCKET
    elif socket.bl_idname == "OCVLRectSocket":
        new_node_idname = settings.DEFAULT_NODE_FOR_QUICK_LINK_RECT_SOCKET
    elif socket.bl_idname == "OCVLContourSocket":
        new_node_idname = settings.DEFAULT_NODE_FOR_QUICK_LINK_CONTOUR_SOCKET
    elif socket.bl_idname == "OCVLVectorSocket":
        new_node_idname = settings.DEFAULT_NODE_FOR_QUICK_LINK_VECTOR_SOCKET
    else:
        new_node_idname = node.n_quick_link_requirements.get(node.inputs[socket.index].name, {}).get("__type_node__")
    if not new_node_idname:
        return
    return new_node_idname


def get_new_output_node_idname(node, socket):
    if socket.bl_idname == "OCVLImageSocket":
        new_node_idname = settings.DEFAULT_NODE_FOR_QUICK_LINK_IMAGE_SOCKET_OUT
    elif socket.bl_idname == "OCVLContourSocket":
        new_node_idname = "OCVLdrawContoursNode"
    elif socket.bl_idname in ["OCVLObjectSocket", "OCVLVectorSocket"]:
        new_node_idname = "OCVLStethoscopeNode"
    else:
        return
    return new_node_idname


class OCVL_OT_LinkNewNodeInput(bpy.types.Operator):
    bl_idname = "ocvl.quick_link_new_node"
    bl_label = "Add a new node to the left"

    child: bpy.props.BoolProperty(default=False)
    socket_index: bpy.props.IntProperty()
    origin: bpy.props.StringProperty()
    is_input_mode: bpy.props.BoolProperty(default=True)
    is_block_quick_link_requirements: bpy.props.BoolProperty(default=True)
    new_node_idname: bpy.props.StringProperty()
    new_node_offsetx: bpy.props.IntProperty(default=-200)
    new_node_offsety: bpy.props.IntProperty(default=0)

    def execute(self, context):
        if self.is_block_quick_link_requirements:
            return {'FINISHED'}

        ocvl_globals.MUTE_LOOKUP_ERROR = True
        tree = context.space_data.edit_tree
        nodes, links = tree.nodes, tree.links

        caller_node = nodes.get(self.origin)
        new_node = nodes.new(self.new_node_idname)
        self.set_location_new_node(new_node, caller_node)
        n_quick_link_requirements = getattr(caller_node, "n_quick_link_requirements", {})
        multi_link = n_quick_link_requirements.get("multi_link", [])
        if self.is_input_mode and not caller_node.inputs[self.socket_index].name in multi_link:
            multi_link = []

        if self.is_input_mode:
            preset_requirements = n_quick_link_requirements.get(caller_node.inputs[self.socket_index].name)
        else:
            preset_requirements = n_quick_link_requirements.get(caller_node.outputs[self.socket_index].name)

        if not multi_link and preset_requirements:
            for requirement in preset_requirements.keys():
                setattr(new_node, requirement, preset_requirements[requirement])

        if self.is_input_mode:
            self._connect_same_type_sockets(links, new_node.outputs, caller_node.inputs, multi_link)
        else:
            self._connect_same_type_sockets(links, new_node.inputs, caller_node.outputs, multi_link)

        if caller_node.parent:
            new_node.parent = caller_node.parent
            loc_xy = new_node.location[:]
            locx, locy = recursive_framed_location_finder(new_node, loc_xy)
            new_node.location = locx, locy

        if self.is_input_mode:
            for input in new_node.inputs:
                new_node_idname = get_new_input_node_idname(node=new_node, socket=input)
                if not new_node_idname:
                    continue
                bpy.ops.ocvl.quick_link_new_node(socket_index=input.index, origin=new_node.name, is_block_quick_link_requirements=False, new_node_idname=new_node_idname, child=True)

        if not self.child:
            settings.MUTE_LOOKUP_ERROR = False

        return {'FINISHED'}

    def set_location_new_node(self, new_node, caller_node):
        if self.is_input_mode:
            self._set_location_for_input(new_node, caller_node)
        else:
            self._set_location_fro_output(new_node, caller_node)

    def _set_location_for_input(self, new_node, caller_node):
        x_offset = settings.DEFAULT_QUICK_LINK_LOCATION_X_OFFSET
        y_offset = settings.DEFAULT_QUICK_LINK_LOCATION_Y_OFFSET
        y_offset_first_node = settings.DEFAULT_QUICK_LINK_LOCATION_Y_OFFSET_FIRST_NODE
        settings
        pixel_size = bpy.context.preferences.system.pixel_size
        node_tree = new_node.id_data
        left_border = caller_node.location[0] - x_offset - new_node.width
        right_border = caller_node.location[0] - x_offset
        empty_location_y = caller_node.location[1] + y_offset_first_node
        for node in node_tree.nodes:
            if node.name == new_node.name:
                continue
            if left_border <= node.location[0] <= right_border or left_border <= node.location[0] + node.width <= right_border:
                if node.location[1] - node.dimensions[1] / pixel_size < empty_location_y:
                    empty_location_y = node.location[1] - node.dimensions[1] / pixel_size
        new_node.location[0] = left_border
        new_node.location[1] = empty_location_y + y_offset

    def _set_location_fro_output(self, new_node, caller_node):
        x_offset = settings.DEFAULT_QUICK_LINK_LOCATION_X_OFFSET
        y_offset = settings.DEFAULT_QUICK_LINK_LOCATION_Y_OFFSET
        y_offset_first_node = settings.DEFAULT_QUICK_LINK_LOCATION_Y_OFFSET_FIRST_NODE
        pixel_size = bpy.context.preferences.system.pixel_size
        node_tree = new_node.id_data
        left_border = caller_node.location[0] + x_offset + caller_node.width
        right_border = caller_node.location[0] + x_offset + caller_node.width + new_node.width
        empty_location_y = caller_node.location[1] + y_offset_first_node
        for node in node_tree.nodes:
            if node.name == new_node.name:
                continue
            if left_border <= node.location[0] <= right_border or left_border <= node.location[0] + node.width <= right_border:
                if node.location[1] - node.dimensions[1] / pixel_size < empty_location_y:
                    empty_location_y = node.location[1] - node.dimensions[1] / pixel_size
        new_node.location[0] = left_border
        new_node.location[1] = empty_location_y + y_offset


    def _connect_same_type_sockets(self, links, new_node_sockets, caller_node_sockets, multi_link):
        if multi_link:
            self._connect_multi_sockets(links, new_node_sockets, caller_node_sockets)
            return
        bl_idname = caller_node_sockets[self.socket_index].bl_idname
        for socket in new_node_sockets:
            if socket.bl_idname == bl_idname or socket.bl_idname == "OCVLStethoscopeSocket":
                links.new(socket, caller_node_sockets[self.socket_index])

    def _connect_multi_sockets(self, links, new_node_sockets, caller_node_sockets):
        for socket_new in new_node_sockets:
            for socket_caller in caller_node_sockets:
                if socket_new.name.split("_")[0] == socket_caller.name.split("_")[0]:
                    links.new(socket_new, caller_node_sockets[socket_caller.index])


class OCVLSocketBase:
    bl_idname = None
    bl_label = None
    draw_socket_color = None

    _map_quick_link_icons = {
        "output": defaultdict(lambda: ["LIGHT", "OUTLINER_OB_LIGHT"],
            {
                "OCVLObjectSocket": ["OUTLINER_DATA_LIGHTPROBE", "OUTLINER_OB_LIGHTPROBE"],
            }
        )
    }

    use_prop: bpy.props.BoolProperty(default=False)
    use_expander: bpy.props.BoolProperty(default=True)
    use_quicklink: bpy.props.BoolProperty(default=True)
    expanded: bpy.props.BoolProperty(default=False)

    prop_name: bpy.props.StringProperty(default='')
    prop_type: bpy.props.StringProperty(default='')
    prop_index: bpy.props.IntProperty()
    custom_draw: bpy.props.StringProperty()

    @property
    def socket_id(self):
        return str(hash(self.id_data.name + self.node.name + self.identifier))

    @property
    def other(self):
        return get_other_socket(self)

    def set_default(self, value):
        if self.prop_name:
            setattr(self.node, self.prop_name, value)

    @property
    def index(self):
        node = self.node
        sockets = node.outputs if self.is_output else node.inputs
        for i, s in enumerate(sockets):
            if s == self:
                return i

    @property
    def extra_info(self):
        return ""

    def sv_set(self, data):
        set_socket(self, data)

    def sv_get(self):
        return get_socket(self)

    def draw_expander_template(self, context, layout, prop_origin, prop_name="prop"):

        if self.bl_idname == "OCVLObjectSocket":
            layout.prop(prop_origin, prop_name)
        else:
            if self.use_expander:
                split = layout.split(factor=.2, align=True)
                c1 = split.column(align=True)
                c2 = split.column(align=True)

                if self.expanded:
                    c1.prop(self, "expanded", icon='TRIA_UP', text='')
                    c1.label(text=self.name[0])
                    c2.prop(prop_origin, prop_name, text="", expand=True)
                else:
                    c1.prop(self, "expanded", icon='TRIA_DOWN', text="")
                    row = c2.row(align=True)
                    if self.bl_idname == "OCVLColorSocket":
                        row.prop(prop_origin, prop_name)
                    else:
                        row.template_component_menu(prop_origin, prop_name, name=self.name)

            else:
                layout.template_component_menu(prop_origin, prop_name, name=self.name)

    def draw_quick_link_input(self, context, layout, node):

        if self.use_quicklink:
            new_node_idname = get_new_input_node_idname(node, self)

            if not new_node_idname:
                return

            icon = "PLUGIN" if node.inputs[self.index].name in node.n_requirements.get("__and__", []) else "SNAP_ON"
            icon = "PARTICLEMODE" if node.n_quick_link_requirements.get("multi_link", [None])[0] == node.inputs[self.index].name else icon
            op = layout.operator('ocvl.quick_link_new_node', text="", icon=icon)
            op.is_block_quick_link_requirements = False
            op.socket_index = self.index
            op.origin = node.name
            op.is_input_mode = True
            op.new_node_idname = new_node_idname
            op.new_node_offsetx = -250 - 40
            op.new_node_offsety = -460 * self.index if icon in ["PLUGIN", "SNAP_ON"] else 0

    def draw_quick_link_output(self, context, layout, node):
        is_block_quick_link_requirements = True

        if self.use_quicklink:
            new_node_idname = get_new_output_node_idname(node, self)
            if not new_node_idname:
                return

            try:
                node.check_input_requirements(node.n_requirements)
                op_icon = self._map_quick_link_icons["output"][self.bl_idname][1]
                is_block_quick_link_requirements = False
            except (Exception, LackRequiredSocketException) as e:
                op_icon = self._map_quick_link_icons["output"][self.bl_idname][0]

            op = layout.operator('ocvl.quick_link_new_node', text="", icon=op_icon)
            op.is_block_quick_link_requirements = is_block_quick_link_requirements
            op.socket_index = self.index
            op.origin = node.name
            op.is_input_mode = False
            op.new_node_idname = new_node_idname
            op.new_node_offsetx = node.width + 80
            op.new_node_offsety = 230 * self.index

    def draw(self, context, layout, node, text):

        if self.is_linked:  # linked INPUT or OUTPUT
            t = text
            if not self.is_output:
                if self.prop_name:
                    prop = node.rna_type.properties.get(self.prop_name, None)
                    t = prop.name if prop else text
            info_text = t + '. ' + get_socket_info(self)
            info_text += self.extra_info
            layout.label(text=info_text)

        elif self.is_output:  # unlinked OUTPUT
            layout.label(text=text)
            self.draw_quick_link_output(context, layout, node)

        else:  # unlinked INPUT
            if self.prop_name:  # has property
                self.draw_expander_template(context, layout, prop_origin=node, prop_name=self.prop_name)

            elif self.use_prop:  # no property but use default prop
                self.draw_expander_template(context, layout, prop_origin=self)

            # elif self.quicklink_func_name:
            #     try:
            #         getattr(node, self.quicklink_func_name)(self, context, layout, node)
            #     except Exception as e:
            #         self.draw_quick_link(context, layout, node)
            #     layout.label(text=text)
            #
            else:  # no property and not use default prop
                self.draw_quick_link_input(context, layout, node)
                layout.label(text=text)

    def draw_color(self, context, node):
        _draw_socket = getattr(self, "draw_socket_color", None)
        return _draw_socket or settings.SOCKET_COLORS.get(self.bl_idname)


class OCVLColorSocket(bpy.types.NodeSocket, OCVLSocketBase):
    '''For color data'''
    bl_idname = "OCVLColorSocket"
    bl_label = "Color Socket"

    prop: bpy.props.FloatVectorProperty(default=(0, 0, 0, 1), size=4, subtype='COLOR', min=0, max=1, update=process_from_socket)
    prop_name: bpy.props.StringProperty(default='')
    use_prop: bpy.props.BoolProperty(default=False)

    def get_prop_data(self):
        if self.prop_name:
            return {"prop_name": self.prop_name}
        elif self.use_prop:
            return {"use_prop": True,
                    "prop": self.prop[:]}
        else:
            return {}

    def sv_get(self, default=sentinel, deepcopy=True, implicit_conversions=None):
        if self.is_linked and not self.is_output:
            return self.convert_data(get_socket(self, deepcopy), implicit_conversions)

        if self.prop_name:
            return [[getattr(self.node, self.prop_name)[:]]]
        elif self.use_prop:
            return [[self.prop[:]]]
        elif default is sentinel:
            raise LackRequiredSocketException(self)
        else:
            return default


class OCVLObjectSocket(bpy.types.NodeSocket, OCVLSocketBase):
    bl_idname = 'OCVLObjectSocket'
    bl_label = 'OCVLObjectSocket'


class OCVLImageSocket(bpy.types.NodeSocket, OCVLSocketBase):
    bl_idname = 'OCVLImageSocket'
    bl_label = 'OCVLImageSocket'


class OCVLMaskSocket(bpy.types.NodeSocket, OCVLSocketBase):
    bl_idname = 'OCVLMaskSocket'
    bl_label = 'OCVLMaskSocket'


class OCVLRectSocket(bpy.types.NodeSocket, OCVLSocketBase):
    bl_idname = 'OCVLRectSocket'
    bl_label = 'OCVLRectSocket'


class OCVLContourSocket(bpy.types.NodeSocket, OCVLSocketBase):
    bl_idname = 'OCVLContourSocket'
    bl_label = 'OCVLContourSocket'


class OCVLVectorSocket(bpy.types.NodeSocket, OCVLSocketBase):
    bl_idname = 'OCVLVectorSocket'
    bl_label = 'OCVLVectorSocket'


class OCVLStethoscopeSocket(bpy.types.NodeSocket, OCVLSocketBase):
    bl_idname = 'OCVLStethoscopeSocket'
    bl_label = 'OCVLStethoscopeSocket'


def register():
    ocvl_register(OCVL_OT_LinkNewNodeInput)
    ocvl_register(OCVLColorSocket)
    ocvl_register(OCVLObjectSocket)
    ocvl_register(OCVLImageSocket)
    ocvl_register(OCVLMaskSocket)
    ocvl_register(OCVLRectSocket)
    ocvl_register(OCVLContourSocket)
    ocvl_register(OCVLVectorSocket)
    ocvl_register(OCVLStethoscopeSocket)


def unregister():
    ocvl_unregister(OCVL_OT_LinkNewNodeInput)
    ocvl_unregister(OCVLColorSocket)
    ocvl_unregister(OCVLObjectSocket)
    ocvl_unregister(OCVLImageSocket)
    ocvl_unregister(OCVLMaskSocket)
    ocvl_unregister(OCVLRectSocket)
    ocvl_unregister(OCVLContourSocket)
    ocvl_unregister(OCVLVectorSocket)
    ocvl_unregister(OCVLStethoscopeSocket)
