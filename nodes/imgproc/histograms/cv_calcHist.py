import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLcalcHistNode(OCVLNodeBase):

    n_doc = "Calculates a histogram of a set of arrays."
    n_requirements = {"__and__": ["images_in", "channels_in", "ranges_in", "histSize_in"]}
    n_quick_link_requirements = {
        "channels_in": {"loc_input_mode": "MANUAL", "loc_manual_input": "(0, 1, 2)"},
        "histSize_in": {"loc_input_mode": "MANUAL", "loc_manual_input": "(8, 8, 8)"},
        "ranges_in": {"loc_input_mode": "MANUAL", "loc_manual_input": "(0, 180, 0, 256, 0, 256)"},
    }

    images_in: bpy.props.StringProperty(name="images_in", default=str(uuid.uuid4()), description="Source arrays. They all should have the same depth, CV_8U or CV_32F , and the same size. Each of them can have an arbitrary number of channels.")
    channels_in: bpy.props.StringProperty(name="channels_in", default=str(uuid.uuid4()), description=" List of the dims channels used to compute the histogram. The first array channels are numerated from 0 to images[0].channels()-1 , the second array channels are counted from images[0].channels() to images[0].channels() + images[1].channels()-1, and so on.")
    mask_in: bpy.props.StringProperty(name="mask_in", default=str(uuid.uuid4()), description="Optional mask. If the matrix is not empty, it must be an 8-bit array of the same size as images[i] . The non-zero mask elements mark the array elements counted in the histogram.")
    histSize_in: bpy.props.StringProperty(name="histSize_in", default=str(uuid.uuid4()), description="Array of histogram sizes in each dimension.")
    ranges_in: bpy.props.StringProperty(name="ranges_in", default=str(uuid.uuid4()), description="Array of the dims arrays of the histogram bin boundaries in each dimension.")
    accumulate_in: bpy.props.BoolProperty(name="accumulate_in", default=False, description="Accumulation flag. If it is set, the histogram is not cleared in the beginning when it is allocated.")

    hist_out: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Output histogram, which is a dense or sparse dims -dimensional array.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "images_in")
        self.inputs.new("OCVLVectorSocket", "channels_in")
        self.inputs.new("OCVLVectorSocket", "histSize_in")
        self.inputs.new("OCVLVectorSocket", "ranges_in")
        self.inputs.new("OCVLMaskSocket", "mask_in")

        self.outputs.new("OCVLObjectSocket", "hist_out")

    def wrapped_process(self):
        mask_in = self.get_from_props("mask_in")
        kwargs = {
            'images_in': [self.get_from_props("images_in")],
            'channels_in': self.get_from_props("channels_in"),
            'mask_in': None if self.is_uuid(mask_in) else mask_in,
            'histSize_in': self.get_from_props("histSize_in"),
            'ranges_in': self.get_from_props("ranges_in"),
            'accumulate_in': self.get_from_props("accumulate_in"),
        }

        hist_out = self.process_cv(fn=cv2.calcHist, kwargs=kwargs)
        self.refresh_output_socket("hist_out", hist_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "accumulate_in")
