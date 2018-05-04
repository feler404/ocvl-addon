import cv2
import numpy as np
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, BORDER_TYPE_ITEMS, COLOR_DEPTH_ITEMS, updateNode, OCVLNode, \
    DEVELOP_STATE_ALPHA


class OCVLsepFilter2dNode(OCVLNode):
    bl_icon = 'FILTER'
    bl_develop_state = DEVELOP_STATE_ALPHA

    _doc = _("Applies a separable linear filter to an image.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image"))

    def get_anchor(self):
        return self.get("anchor", (-1, -1))

    def set_anchor(self, value):
        anchor_x = value[0] if -1 <= value[0] < self.kernel_size_in[0] else self.anchor_in[0]
        anchor_y = value[1] if -1 <= value[1] < self.kernel_size_in[1] else self.anchor_in[1]
        self["anchor"] = (anchor_x, anchor_y)


    kernel_size_in = IntVectorProperty(default=(1, 1), update=updateNode, min=1, max=30, size=2,
        description=_("Coefficients for filtering each row and column."))
    ddepth_in = EnumProperty(items=COLOR_DEPTH_ITEMS, default='CV_8U', update=updateNode,
        description=_("Destination image depth, see @ref filter_depths 'combinations'"))
    anchor_in = IntVectorProperty(default=(-1, -1), update=updateNode, get=get_anchor, set=set_anchor, size=2,
        description=_("Anchor position within the kernel. The default value \f$(-1,-1)\f$ means that the anchor is at the kernel center."))
    delta_in = IntProperty(default=0, update=updateNode, min=0, max=255,
        description=_("Value added to the filtered results before storing them."))
    borderType_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description=_("Pixel extrapolation method, see cv::BorderTypes"))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "kernel_size_in").prop_name = 'kernel_size_in'
        self.inputs.new('StringsSocket', "anchor_in").prop_name = 'anchor_in'
        self.inputs.new('StringsSocket', "delta_in").prop_name = 'delta_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kernel_width, kernel_height = self.get_from_props("kernel_size_in")
        kernelX_in = kernelY_in = np.ones((kernel_width, kernel_height), np.float32) / kernel_width * kernel_height
        kwargs = {
            'src': self.get_from_props("image_in"),
            'ddepth_in': self.get_from_props("ddepth_in"),
            'delta_in': self.get_from_props("delta_in"),
            'kernelX_in': kernelX_in,
            'kernelY_in': kernelY_in,
            'anchor_in': self.get_from_props("anchor_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        image_out = self.process_cv(fn=cv2.sepFilter2D, kwargs=kwargs)

        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'ddepth_in')
        self.add_button(layout, 'borderType_in')


def register():
    cv_register_class(OCVLsepFilter2dNode)


def unregister():
    cv_unregister_class(OCVLsepFilter2dNode)
