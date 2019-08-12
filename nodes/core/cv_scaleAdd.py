import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLscaleAddNode(OCVLNodeBase):

    n_doc = "Calculates the sum of a scaled array and another array."
    n_requirements = {"__and__": ["src1_in", "src2_in"]}

    src1_in: bpy.props.StringProperty(name="src1_in", default=str(uuid.uuid4()),  description="First input array.")
    src2_in: bpy.props.StringProperty(name="src2_in", default=str(uuid.uuid4()),  description="Second input array of the same size and type as src1.")
    alpha_in: bpy.props.FloatProperty(name="alpha_in", default=3, min=0, max=100, update=update_node, description="Scale factor for the first array.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same type as src.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src1_in")
        self.inputs.new("OCVLImageSocket", "src2_in")
        self.inputs.new("OCVLMatrixSocket", "alpha_in").prop_name = "alpha_in"

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src1_in': self.get_from_props("src1_in"),
            'src2_in': self.get_from_props("src2_in"),
            'alpha_in': self.get_from_props("alpha_in"),
            }

        dst_out = self.process_cv(fn=cv2.scaleAdd, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
