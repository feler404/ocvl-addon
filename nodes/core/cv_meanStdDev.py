import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLmeanStdDevNode(OCVLNodeBase):

    n_doc = "Calculates a mean and standard deviation of array elements."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array that should have from 1 to 4 channels so that the results can be stored in Scalar_ ‘s.")
    mask_in: bpy.props.StringProperty(name="mask_in", default=str(uuid.uuid4()), description="Optional operation mask.")

    mean_out: bpy.props.StringProperty(name="array_out", default=str(uuid.uuid4()), description="Output parameter: calculated mean value.")
    stddev_out: bpy.props.StringProperty(name="array_out", default=str(uuid.uuid4()), description="Output parameter: calculateded standard deviation.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLMaskSocket", "mask_in")
        self.outputs.new("OCVLImageSocket", "mean_out")
        self.outputs.new("OCVLImageSocket", "stddev_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'mask_in': self.get_from_props("mask_in"),
            }

        mean_out, stddev_out = self.process_cv(fn=cv2.meanStdDev, kwargs=kwargs)
        self.refresh_output_socket("mean_out", mean_out, is_uuid_type=True)
        self.refresh_output_socket("stddev_out", stddev_out, is_uuid_type=True)
