import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntVectorProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, BORDER_TYPE_ITEMS, COLOR_DEPTH_ITEMS, OCVLNode, updateNode


class OCVLboxFilterNode(OCVLNode):

    _doc = _("Blurs an image using the box filter.")

    bl_icon = 'FILTER'

    def get_anchor(self):
        return self.get("anchor_in", (-1, -1))

    def set_anchor(self, value):
        anchor_x = value[0] if -1 <= value[0] < self.ksize_in[0] else self.anchor_in[0]
        anchor_y = value[1] if -1 <= value[1] < self.ksize_in[1] else self.anchor_in[1]
        self["anchor_in"] = (anchor_x, anchor_y)

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    ksize_in = IntVectorProperty(default=(3, 3), min=1, max=30, size=2, update=updateNode,
        description=_("Blurring kernel size."))
    anchor_in = IntVectorProperty(default=(-1, -1), update=updateNode, get=get_anchor, set=set_anchor, size=2,
        description=_("Anchor point."))
    ddepth_in = EnumProperty(items=COLOR_DEPTH_ITEMS, default='CV_8U', update=updateNode,
        description=_("The output image depth."))
    normalize_in = BoolProperty(default=True, update=updateNode,
        description=_("Flag, specifying whether the kernel is normalized by its area or not."))
    borderType_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description=_("Pixel extrapolation method, see cv::BorderTypes"))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('StringsSocket', "anchor_in").prop_name = 'anchor_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
            'ksize_in': self.get_from_props("ksize_in"),
            'anchor_in': self.get_from_props("anchor_in"),
            'ddepth_in': self.get_from_props("ddepth_in"),
            'normalize_in': self.get_from_props("normalize_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        image_out = self.process_cv(fn=cv2.boxFilter, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "ddepth_in")
        self.add_button(layout, "normalize_in")
        self.add_button(layout, "borderType_in")


def register():
    cv_register_class(OCVLboxFilterNode)


def unregister():
    cv_unregister_class(OCVLboxFilterNode)
