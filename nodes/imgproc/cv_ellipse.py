import cv2
import uuid

from bpy.props import EnumProperty, StringProperty, IntProperty, FloatVectorProperty, IntVectorProperty

from ...extend.utils import cv_register_class, cv_unregister_class, LINE_TYPE_ITEMS, OCVLNode, updateNode


INPUT_NODE_ITEMS = (
    ("FULL", "FULL", "FULL", "", 0),
    ("SIMPLE", "SIMPLE", "SIMPLE", "", 1),
)


PROPS_MAPS = {
    INPUT_NODE_ITEMS[0][0]: ("center_in", "axes_in", "angle_in", "startAngle_in", "endAngle_in"),
    INPUT_NODE_ITEMS[1][0]: ("box_in",),
    }


class OCVLellipseNode(OCVLNode):
    bl_icon = 'GREASEPENCIL'

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    def update_layout(self, context):
        self.update_sockets(context)
        updateNode(self,context)

    # INPUT MODE PROPERTIES
    box_in = StringProperty(default=str(uuid.uuid4()),
        description="Alternative ellipse representation via RotatedRect. This means that the function draws an ellipse inscribed in the rotated rectangle.")

    center_in = IntVectorProperty(default=(0, 0), size=2, update=updateNode,
        description="Center of the ellipse.")
    axes_in = IntVectorProperty(default=(1, 1), size=2, min=0, max=1000, update=updateNode,
        description="Half of the size of the ellipse main axes.")
    angle_in = IntProperty(default=30, min=0, max=360, update=updateNode,
        description="Ellipse rotation angle in degrees.")
    startAngle_in = IntProperty(default=0, min=0, max=360, update=updateNode,
        description="Starting angle of the elliptic arc in degrees.")
    endAngle_in = IntProperty(default=270, min=0, max=360, update=updateNode,
        description="Ending angle of the elliptic arc in degrees")

    # COMMON PROPERTIES
    color_in = FloatVectorProperty(update=updateNode, default=(.7, .7, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR',
        description="Ellipse color.")
    thickness_in = IntProperty(default=2, min=-1, max=10, update=updateNode,
        description="Thickness of the ellipse arc outline, if positive. Otherwise, this indicates that a filled ellipse sector is to be drawn.")
    lineType_in = EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA",update=updateNode,
        description="Type of the ellipse boundary. See the line description.")
    loc_input_mode = EnumProperty(items=INPUT_NODE_ITEMS, default="SIMPLE", update=update_layout)

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('SvColorSocket', 'color_in').prop_name = 'color_in'
        self.inputs.new('StringsSocket', "thickness_in").prop_name = 'thickness_in'

        self.outputs.new("StringsSocket", "image_out")
        self.update_layout(context)

    def update_sockets(self, context):
        self.update_sockets_for_node_mode(PROPS_MAPS, self.loc_input_mode)
        self.process()

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])
        self.check_inputs_requirements_mode(requirements=(("box_in", "SIMPLE"),), props_maps=PROPS_MAPS, input_mode=self.loc_input_mode)
        kwargs_inputs= self.get_kwargs_inputs(PROPS_MAPS, self.loc_input_mode)

        kwargs = {
            'img_in': self.get_from_props("image_in"),
            'color_in': self.get_from_props("color_in"),
            'thickness_in': self.get_from_props("thickness_in"),
            'lineType_in': self.get_from_props("lineType_in"),
            }
        kwargs.update(kwargs_inputs)

        image_out = self.process_cv(fn=cv2.ellipse, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'lineType_in')
        self.add_button(layout, 'loc_input_mode', expand=True)


def register():
    cv_register_class(OCVLellipseNode)


def unregister():
    cv_unregister_class(OCVLellipseNode)
