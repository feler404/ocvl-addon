import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatVectorProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, LINE_TYPE_ITEMS, updateNode

INPUT_MODE_ITEMS = (
    ("X, Y, W, H", "X, Y, W, H", "X, Y, W, H", "", 0),
    ("PT1, PT2", "PT1, PT2", "PT1, PT2", "", 1),
    ("Rect", "Rect", "Rect", "", 2),
)


PROPS_MAPS = {
    INPUT_MODE_ITEMS[0][0]: ("x_in", "y_in", "w_in", "h_in"),
    INPUT_MODE_ITEMS[1][0]: ("pt1_in", "pt2_in"),
    INPUT_MODE_ITEMS[2][0]: ("rect_in",),
}


class OCVLrectangleNode(OCVLNode):
    bl_icon = 'GREASEPENCIL'

    _doc = _("Draws a simple, thick, or filled up-right rectangle.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))

    def update_layout(self, context):
        self.update_sockets(context)
        updateNode(self, context)

    # INPUT MODE PROPERTIES
    pt1_in = IntVectorProperty(default=(0, 0), size=2, update=updateNode,
        description=_("Vertex of the rectangle."))
    pt2_in = IntVectorProperty(default=(1, 1), size=2, update=updateNode,
        description=_("Vertex of the rectangle opposite to pt1."))

    x_in = IntProperty(default=0, update=updateNode,
        description=_("X for point of top left corner."))
    y_in = IntProperty(default=0, update=updateNode,
        description=_("Y for point of top left corner."))
    w_in = IntProperty(default=0, update=updateNode,
        description=_("Weight of rectangle."))
    h_in = IntProperty(default=0, update=updateNode,
        description=_("Height of rectangle."))

    rect_in = IntVectorProperty(default=(0, 0, 0, 0), size=4, update=updateNode,
        description=_("X, Y, Weight, Height in one vector."))

    # COMMON PROPERTIES
    color_in = FloatVectorProperty(update=updateNode, default=(.7, .7, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR',
        description=_("Rectangle color or brightness (grayscale image)."))
    thickness_in = IntProperty(default=2, min=-1, max=10, update=updateNode,
        description=_("Thickness of lines that make up the rectangle. Negative values, like CV_FILLED, mean that the function has to draw a filled rectangle."))
    lineType_in = EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA",update=updateNode,
        description=_("Type of the line. See the line description."))
    shift_in = IntProperty(default=0, min=1, max=100, update=updateNode,
        description=_("Number of fractional bits in the point coordinates."))
    loc_input_mode = EnumProperty(items=INPUT_MODE_ITEMS, default="PT1, PT2", update=update_layout,
        description=_("Loc input mode."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('SvColorSocket', 'color_in').prop_name = 'color_in'
        self.inputs.new('StringsSocket', "thickness_in").prop_name = 'thickness_in'
        self.inputs.new('StringsSocket', "shift_in").prop_name = 'shift_in'

        self.outputs.new("StringsSocket", "image_out")
        self.update_layout(context)

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])
        pt1_in, pt2_in = self._get_inputs_points(self.loc_input_mode)

        kwargs = {
            'img_in': self.get_from_props("image_in"),
            'pt1_in': pt1_in,
            'pt2_in': pt2_in,
            'color_in': self.get_from_props("color_in"),
            'thickness_in': self.get_from_props("thickness_in"),
            'lineType_in': self.get_from_props("lineType_in"),
            'shift_in': self.get_from_props("shift_in"),
            }

        image_out = self.process_cv(fn=cv2.rectangle, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def update_sockets(self, context):
        self.update_sockets_for_node_mode(PROPS_MAPS, self.loc_input_mode)
        self.process()

    def _get_inputs_points(self, input_mode):
        val = []
        for prop_name in PROPS_MAPS[input_mode]:
            prop_value = self.get_from_props(prop_name)
            if isinstance(prop_value, (list, tuple)):
                val.extend(prop_value)
            else:
                val.append(prop_value)
        return tuple(val[:2]), tuple(val[2:])

    def draw_buttons(self, context, layout):
        self.add_button(layout=layout, prop_name='lineType_in')
        self.add_button(layout=layout, prop_name='loc_input_mode', expand=True)
        if self.loc_input_mode == "PT1, PT2":
            self.add_button_get_points(layout=layout, props_name=('pt1_in', 'pt2_in'))


def register():
    cv_register_class(OCVLrectangleNode)


def unregister():
    cv_unregister_class(OCVLrectangleNode)
