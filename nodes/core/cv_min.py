import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase


class OCVLminNode(OCVLNodeBase):

    n_doc = "Calculates per-element minimum of two arrays or an array and a scalar."
    n_requirements = {"__and__": ["src1_in", "src2_in"]}

    src1_in: bpy.props.StringProperty(name="src1_in", default=str(uuid.uuid4()), description="First input array.")
    src2_in: bpy.props.StringProperty(name="src2_in", default=str(uuid.uuid4()), description="Second input array of the same size and type as src1.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same size and type as src1.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src1_in")
        self.inputs.new("ImageSocket", "src2_in")
        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src1_in': self.get_from_props("src1_in"),
            'src2_in': self.get_from_props("src2_in"),
            }

        dst_out = self.process_cv(fn=cv2.min, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
