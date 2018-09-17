import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, FloatProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


SOBEL_SIZE_ITEMS = (
    ("3", "3", "3", "", 0),
    ("5", "5", "5", "", 1),
    ("7", "7", "7", "", 2),
)


class OCVLCannyNode(OCVLNode):

    _doc = _("Finds edges in an image using the [Canny86] algorithm.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("8-bit input image."))
    threshold1_in = FloatProperty(default=100, min=0, max=255, update=updateNode,
        description=_("First threshold for the hysteresis procedure."))
    threshold2_in = FloatProperty(default=200, min=0, max=255, update=updateNode,
        description=_("Second threshold for the hysteresis procedure."))
    apertureSize_in = EnumProperty(items=SOBEL_SIZE_ITEMS, default="3", update=updateNode,
        description=_("Aperture size for the Sobel operator."))
    L2gradient_in = BoolProperty(default=False, update=updateNode,
        description=_("Flag, indicating whether a more accurate."))

    edges_out = StringProperty(name="edges_out", default=str(uuid.uuid4()),
        description=_("Output edge map. Single channels 8-bit image, which has the same size as image."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "threshold1_in").prop_name = 'threshold1_in'
        self.inputs.new('StringsSocket', "threshold2_in").prop_name = 'threshold2_in'

        self.outputs.new("StringsSocket", "edges_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'threshold1_in': self.get_from_props("threshold1_in"),
            'threshold2_in': self.get_from_props("threshold2_in"),
            'apertureSize_in': int(self.get_from_props("apertureSize_in")),
            'L2gradient_in': self.get_from_props("L2gradient_in"),
            }

        edges_out = self.process_cv(fn=cv2.Canny, kwargs=kwargs)
        self.refresh_output_socket("edges_out", edges_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'L2gradient_in')
        self.add_button(layout, 'apertureSize_in', expand=True)


def register():
    cv_register_class(OCVLCannyNode)


def unregister():
    cv_unregister_class(OCVLCannyNode)
