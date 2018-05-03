import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatVectorProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, LINE_TYPE_ITEMS, OCVLNode, updateNode


class OCVLcircleNode(OCVLNode):
    bl_icon = 'GREASEPENCIL'

    _doc = _("Draws a circle.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))

    center_in = IntVectorProperty(default=(0, 0), size=2, update=updateNode,
        description=_("Center of the circle."))
    radius_in = IntProperty(default=50, min=1, max=100, update=updateNode,
        description=_("Radius of the circle."))
    color_in = FloatVectorProperty(update=updateNode, default=(.7, .7, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR',
        description=_("Circle color."))
    thickness_in = IntProperty(default=2, min=-1, max=10, update=updateNode,
        description=_("Thickness of the circle outline, if positive. Negative thickness means that a filled circle is to be drawn."))
    lineType_in = EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA",update=updateNode,
        description=_("Type of the circle boundary. See the line description."))
    shift_in = IntProperty(default=0, min=0, max=10, update=updateNode,
        description=_("Number of fractional bits in the coordinates of the center and in the radius value."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "center_in").prop_name = 'center_in'
        self.inputs.new('StringsSocket', "radius_in").prop_name = 'radius_in'
        self.inputs.new('SvColorSocket', 'color_in').prop_name = 'color_in'
        self.inputs.new('StringsSocket', "thickness_in").prop_name = 'thickness_in'
        self.inputs.new('StringsSocket', "shift_in").prop_name = 'shift_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'img_in': self.get_from_props("image_in"),
            'center_in': self.get_from_props("center_in"),
            'color_in': self.get_from_props("color_in"),
            'thickness_in': self.get_from_props("thickness_in"),
            'radius_in': self.get_from_props("radius_in"),
            'lineType_in': self.get_from_props("lineType_in"),
            'shift_in': self.get_from_props("shift_in"),
            }

        image_out = self.process_cv(fn=cv2.circle, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'lineType_in')


def register():
    cv_register_class(OCVLcircleNode)


def unregister():
    cv_unregister_class(OCVLcircleNode)
