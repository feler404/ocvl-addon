import cv2
import numpy as np
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, BORDER_TYPE_ITEMS, COLOR_DEPTH_ITEMS, updateNode, OCVLNode


class OCVLfilter2dNode(OCVLNode):
    bl_icon = 'FILTER'

    _doc = _("Convolves an image with the kernel.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))

    def get_anchor(self):
        return self.get("anchor", (-1, -1))

    def set_anchor(self, value):
        anchor_x = value[0] if -1 <= value[0] < self.kernel_size[0] else self.anchor[0]
        anchor_y = value[1] if -1 <= value[1] < self.kernel_size[1] else self.anchor[1]
        self["anchor"] = (anchor_x, anchor_y)


    kernel_size = IntVectorProperty(default=(1, 1), update=updateNode, min=1, max=30, size=2,
        description=_("Convolution kernel (or rather a correlation kernel), a single-channel floating point matrix; if you want to apply different kernels to different channels, split the image into separate color planes using split and process them individually."))
    ddepth = EnumProperty(items=COLOR_DEPTH_ITEMS, default='CV_8U', update=updateNode,
        description=_("Desired depth of the destination image, see @ref filter_depths 'combinations'"))
    anchor = IntVectorProperty(default=(-1, -1), update=updateNode, get=get_anchor, set=set_anchor, size=2,
        description=_("Anchor of the kernel that indicates the relative position of a filtered point within the kernel; the anchor should lie within the kernel; default value (-1,-1) means that the anchor is at the kernel center."))
    delta = IntProperty(default=0, update=updateNode, min=0, max=255,
        description=_("Optional value added to the filtered pixels before storing them in dst."))
    borderType = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description=_("Pixel extrapolation method, see cv::BorderTypes"))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "kernel_size").prop_name = 'kernel_size'
        self.inputs.new('StringsSocket', "anchor").prop_name = 'anchor'
        self.inputs.new('StringsSocket', "delta").prop_name = 'delta'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kernel_width, kernel_height = self.get_from_props("kernel_size")
        kernel = np.ones((kernel_width, kernel_height), np.float32) / kernel_width * kernel_height
        kwargs = {
            'src': self.get_from_props("image_in"),
            'ddepth': self.get_from_props("ddepth"),
            'delta': self.get_from_props("delta"),
            'kernel': kernel,
            'anchor': self.get_from_props("anchor"),
            'borderType': self.get_from_props("borderType"),
            }

        image_out = self.process_cv(fn=cv2.filter2D, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'ddepth')
        self.add_button(layout, 'borderType')


def register():
    cv_register_class(OCVLfilter2dNode)


def unregister():
    cv_unregister_class(OCVLfilter2dNode)
