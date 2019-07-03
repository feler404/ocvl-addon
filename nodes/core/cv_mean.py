import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLmeanNode(OCVLNodeBase):

    n_doc = "Calculates an average (mean) of array elements."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array that should have from 1 to 4 channels so that the result can be stored in Scalar_. ")
    mask_in: bpy.props.StringProperty(name="mask_in", default=str(uuid.uuid4()), description="Optional operation mask.")

    retval_out: bpy.props.StringProperty(name="retval_out", default=str(uuid.uuid4()), description="Output parameter: calculated mean value.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new("MaskSocket", "mask_in")
        self.outputs.new("VectorSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'mask_in': self.get_from_props("mask_in"),
            }

        retval_out = self.process_cv(fn=cv2.mean, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass
