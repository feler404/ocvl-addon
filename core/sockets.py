from copy import deepcopy

import bpy
from ocvl.core.exceptions import NoDataError
from ocvl.core.globals import SOCKET_DATA_CACHE
from ocvl.core.register_utils import ocvl_register, ocvl_unregister


def get_other_socket(socket):
    """
    Get next real upstream socket.
    This should be expanded to support wifi nodes also.
    Will return None if there isn't a another socket connect
    so no need to check socket.links
    """
    if not socket.is_linked:
        return None
    if not socket.is_output:
        other = socket.links[0].from_socket
    else:
        other = socket.links[0].to_socket

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
        s_id = other.socket_id
        s_ng = other.id_data.name
        if s_ng not in SOCKET_DATA_CACHE:
            raise LookupError
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
            raise NoDataError(socket)
    # not linked
    raise NoDataError(socket)



def SvGetSocketInfo(socket):
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


class OCVLSocket():
    use_prop = bpy.props.BoolProperty(default=False)
    use_expander = bpy.props.BoolProperty(default=True)
    use_quicklink = bpy.props.BoolProperty(default=True)
    expanded = bpy.props.BoolProperty(default=False)

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

        if self.bl_idname == "StringsSocket":
            layout.prop(prop_origin, prop_name)
        else:
            if self.use_expander:
                split = layout.split(percentage=.2, align=True)
                c1 = split.column(align=True)
                c2 = split.column(align=True)

                if self.expanded:
                    c1.prop(self, "expanded", icon='TRIA_UP', text='')
                    c1.label(text=self.name[0])
                    c2.prop(prop_origin, prop_name, text="", expand=True)
                else:
                    c1.prop(self, "expanded", icon='TRIA_DOWN', text="")
                    row = c2.row(align=True)
                    if self.bl_idname == "SvColorSocket":
                        row.prop(prop_origin, prop_name)
                    else:
                        row.template_component_menu(prop_origin, prop_name, name=self.name)

            else:
                layout.template_component_menu(prop_origin, prop_name, name=self.name)

    def draw_quick_link(self, context, layout, node):

        if self.use_quicklink:
            if self.bl_idname == "MatrixSocket":
                new_node_idname = "SvMatrixGenNodeMK2"
            elif self.bl_idname == "VerticesSocket":
                new_node_idname = "GenVectorsNode"
            else:
                return

            # op = layout.operator('node.sv_quicklink_new_node_input', text="", icon="PLUGIN")
            # op.socket_index = self.index
            # op.origin = node.name
            # op.new_node_idname = new_node_idname
            # op.new_node_offsetx = -200 - 40 * self.index
            # op.new_node_offsety = -30 * self.index

    def draw(self, context, layout, node, text):

        if self.is_linked:  # linked INPUT or OUTPUT
            t = text
            if not self.is_output:
                if self.prop_name:
                    prop = node.rna_type.properties.get(self.prop_name, None)
                    t = prop.name if prop else text
            info_text = t + '. ' + SvGetSocketInfo(self)
            info_text += self.extra_info
            layout.label(info_text)

        elif self.is_output:  # unlinked OUTPUT
            layout.label(text)

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
            #     layout.label(text)
            #
            else:  # no property and not use default prop
                self.draw_quick_link(context, layout, node)
                layout.label(text)


class StringsSocket(bpy.types.NodeSocket, OCVLSocket):
    '''Renderman co-shader input/output'''
    bl_idname = 'StringsSocket'
    bl_label = 'StringsSocket'

    uuid = bpy.props.StringProperty(default="")
    prop_name = bpy.props.StringProperty(default='')

    prop_type = bpy.props.StringProperty(default='')
    prop_index = bpy.props.IntProperty()

    custom_draw = bpy.props.StringProperty()

    def draw_value(self, context, layout, node):
        layout.label(self.name)

    def draw_color(self, context, node):
        return (0.1, 1.0, 0.2, 1)


def register():
    ocvl_register(StringsSocket)


def unregister():
    ocvl_unregister(StringsSocket)
