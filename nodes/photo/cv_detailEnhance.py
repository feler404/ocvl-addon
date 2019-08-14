import uuid

import bpy
import cv2
import numpy as np
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLdetailEnhanceNode(OCVLNodeBase):

    n_doc = "Equalizes the histogram of a grayscale image."
    n_requirements = {"__and__": {"src_in": {"type": np.ndarray, "dtype": "uint8", "channels": 3}}}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input 8-bit 3-channel image.")
    sigma_s_in: bpy.props.FloatProperty(name="sigma_s_in ", default=5, min=0, max=200, update=update_node, description="Range between 0 to 200.")
    sigma_r_in: bpy.props.FloatProperty(name="sigma_r_in", default=1, min=0, max=1, step=0.01, update=update_node, description="Range between 0 to 1.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image with the same size and type as src.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLObjectSocket", "sigma_s_in").prop_name = "sigma_s_in"
        self.inputs.new("OCVLObjectSocket", "sigma_r_in").prop_name = "sigma_r_in"

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("src_in"),
            'sigma_s_in': self.get_from_props("sigma_s_in"),
            'sigma_r_in': self.get_from_props("sigma_r_in"),
        }

        dst_out = self.process_cv(fn=cv2.detailEnhance, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
