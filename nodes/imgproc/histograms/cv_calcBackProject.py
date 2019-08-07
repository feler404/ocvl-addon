import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLcalcBackProjectNode(OCVLNodeBase):

    n_doc = "The functions calcBackProject calculate the back project of the histogram. That is, similarly to calcHist , at each location (x, y) the function collects the values from the selected channels in the input images and finds the corresponding histogram bin. But instead of incrementing it, the function reads the bin value, scales it by scale , and stores in backProject(x,y) . "
    n_requirements = {"__and__": ["images_in", "channels_in", "ranges_in", "hist_in"]}
    n_quick_link_requirements = {
        "channels_in": {"loc_input_mode": "MANUAL", "loc_manual_input": "(0, 1, 2)"},
        "hist_in": {"loc_input_mode": "MANUAL", "loc_manual_input": "(8, 8, 8)"},
        "ranges_in": {"loc_input_mode": "MANUAL", "loc_manual_input": "(0, 180, 0, 256, 0, 256)"},
    }

    images_in: bpy.props.StringProperty(name="images_in", default=str(uuid.uuid4()), description="Source arrays. They all should have the same depth, CV_8U or CV_32F , and the same size. Each of them can have an arbitrary number of channels.")
    channels_in: bpy.props.StringProperty(name="channels_in", default=str(uuid.uuid4()), description="The list of channels used to compute the back projection. The number of channels must match the histogram dimensionality.")
    hist_in: bpy.props.StringProperty(name="hist_in", default=str(uuid.uuid4()), description="Input histogram that can be dense or sparse.")
    ranges_in: bpy.props.StringProperty(name="ranges_in", default=str(uuid.uuid4()), description="Array of arrays of the histogram bin boundaries in each dimension. See calcHist() .")
    scale_in: bpy.props.FloatProperty(name="scale_in", default=float(uuid.uuid4()), description="Optional scale factor for the output back projection.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Calculates the back projection of a histogram.")

    def init(self, context):
        self.inputs.new("ImageSocket", "images_in")
        self.inputs.new("VectorSocket", "channels_in")
        self.inputs.new("VectorSocket", "hist_in")
        self.inputs.new("VectorSocket", "ranges_in")
        self.inputs.new("StringsSocket", "scale_in")

        self.outputs.new("StringsSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'images_in': [self.get_from_props("images_in")],
            'channels_in': self.get_from_props("channels_in"),
            'hist_in': self.get_from_props("hist_in"),
            'ranges_in': self.get_from_props("ranges_in"),
            'scale_in': self.get_from_props("scale_in"),
        }

        dst_out = self.process_cv(fn=cv2.calcBackProject, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)