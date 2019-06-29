import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLconvertScaleAbsNode(OCVLNodeBase):

    n_doc = "Scales, calculates absolute values, and converts the result to 8-bit."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image.")
    alpha_in: bpy.props.FloatProperty(default=1, min=0.0, max=100, update=update_node, description="Optional scale factor.")
    beta_in: bpy.props.FloatProperty(default=0, min=0.0, max=100, update=update_node, description="Optional delta added to the scaled values.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new('StringsSocket', "alpha_in").prop_name = 'alpha_in'
        self.inputs.new('StringsSocket', "beta_in").prop_name = 'beta_in'

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):

        kwargs = {
            'src': self.get_from_props("src_in"),
            'alpha_in': self.get_from_props("alpha_in"),
            'beta_in': self.get_from_props("beta_in"),
            }

        dst_out = self.process_cv(fn=cv2.convertScaleAbs, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
