import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLpencilSketchNode(OCVLNodeBase):

    n_doc = "Pencil-like non-photorealistic line drawing"
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input 8-bit 3-channel image.")
    sigma_s_in: bpy.props.FloatProperty(name="sigma_s_in ", default=5, min=0, max=200, update=update_node, description="Range between 0 to 200.")
    sigma_r_in: bpy.props.FloatProperty(name="sigma_r_in", default=1, min=0, max=1, step=0.01, update=update_node, description="Range between 0 to 1.")
    shade_factor_in: bpy.props.FloatProperty(name="sigma_r_in", default=0.02, min=0, max=0.1, step=0.01, update=update_node, description="Range between 0 to 1.")

    dst1_out: bpy.props.StringProperty(name="dst1_out", default=str(uuid.uuid4()), description="Output 8-bit 1-channel image.")
    dst2_out: bpy.props.StringProperty(name="dst2_out", default=str(uuid.uuid4()), description="Output image with the same size and type as src.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLObjectSocket", "sigma_s_in").prop_name = "sigma_s_in"
        self.inputs.new("OCVLObjectSocket", "sigma_r_in").prop_name = "sigma_r_in"
        self.inputs.new("OCVLObjectSocket", "shade_factor_in").prop_name = "shade_factor_in"

        self.outputs.new("OCVLImageSocket", "dst1_out")
        self.outputs.new("OCVLImageSocket", "dst2_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'sigma_s_in': self.get_from_props("sigma_s_in"),
            'sigma_r_in': self.get_from_props("sigma_r_in"),
            'shade_factor_in': self.get_from_props("shade_factor_in"),
        }

        dst1_out, dst2_out = self.process_cv(fn=cv2.pencilSketch, kwargs=kwargs)
        self.refresh_output_socket("dst1_out", dst1_out, is_uuid_type=True)
        self.refresh_output_socket("dst2_out", dst2_out, is_uuid_type=True)
