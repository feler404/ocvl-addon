import cv2
import uuid
import numpy as np
from bpy.props import StringProperty, BoolProperty, IntVectorProperty, FloatVectorProperty

from ...extend.utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


ADAPTIVE_METHOD_ITEMS = (
    ("ADAPTIVE_THRESH_GAUSSIAN_C", "ADAPTIVE_THRESH_GAUSSIAN_C", "ADAPTIVE_THRESH_GAUSSIAN_C", "", 0),
    ("ADAPTIVE_THRESH_MEAN_C", "ADAPTIVE_THRESH_MEAN_C", "ADAPTIVE_THRESH_MEAN_C", "", 1),
)

KERNEL_SIZE_ITEMS = (
    ("3", "3", "3", "", 0),
    ("5", "5", "5", "", 1),
    ("7", "7", "7", "", 2),
)


class OCVLfloodFillNode(OCVLNode):

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description="Source 8-bit single-channel image.")
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description="Destination image of the same size and the same type as src.")
    rect_out = IntVectorProperty(default=(0, 0, 1, 1), size=4)

    seedPoint_in = IntVectorProperty(default=(0, 0), size=2, update=updateNode,
        description="Starting point.")
    newVal_in = FloatVectorProperty(update=updateNode, default=(.1, .1, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR',
        description="New value of the repainted domain pixels.")
    loDiff_in = FloatVectorProperty(update=updateNode, default=(.1, .1, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR',
        description="Maximal lower brightness/color difference between the currently observed pixel and one of its neighbors belonging to the component, or a seed pixel being added to the component.")
    upDiff_in = FloatVectorProperty(update=updateNode, default=(.9, .9, .9, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR',
        description="Maximal upper brightness/color difference between the currently observed pixel and one of its neighbors belonging to the component, or a seed pixel being added to the component.")
    flag_fixed_range_in = BoolProperty(default=False, update=updateNode,
        description="If set, the difference between the current pixel and seed pixel is considered. Otherwise, the difference between neighbor pixels is considered (that is, the range is floating).")
    flag_mask_only_in = BoolProperty(default=False, update=updateNode,
        description="If set, the function does not change the image ( newVal is ignored), and only fills the mask with the value specified in bits 8-16 of flags as described above.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "seedPoint_in").prop_name = "seedPoint_in"
        self.inputs.new("SvColorSocket", "newVal_in").prop_name = "newVal_in"
        self.inputs.new("SvColorSocket", "loDiff_in").prop_name = "loDiff_in"
        self.inputs.new("SvColorSocket", "upDiff_in").prop_name = "upDiff_in"

        self.outputs.new("StringsSocket", "image_out")
        self.outputs.new("StringsSocket", "mask_out")
        self.outputs.new("StringsSocket", "rect_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        image_in = self.get_from_props("image_in")
        h, w = image_in.shape[:2]
        mask_in = np.zeros((h + 2, w + 2), np.uint8)
        kwargs = {
            'image_in': image_in,
            'mask_in': mask_in,
            'seedPoint_in': self.get_from_props("seedPoint_in"),
            'newVal_in': self.get_from_props("newVal_in", is_color=True),
            'loDiff_in': self.get_from_props("loDiff_in", is_color=True),
            'upDiff_in': self.get_from_props("upDiff_in", is_color=True),
            }

        retval, image_out, mask_out, rect_out = self.process_cv(fn=cv2.floodFill, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)
        self.refresh_output_socket("mask_out", mask_out, is_uuid_type=True)
        self.refresh_output_socket("rect_out", rect_out)

    def draw_buttons(self, context, layout):
        self.add_button_get_points(layout=layout, props_name=('seedPoint_in',))


def register():
    cv_register_class(OCVLfloodFillNode)


def unregister():
    cv_unregister_class(OCVLfloodFillNode)
