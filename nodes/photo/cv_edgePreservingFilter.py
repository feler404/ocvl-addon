import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLedgePreservingFilterNode(OCVLNodeBase):

    bl_flags_list = 'RECURS_FILTER, NORMCONV_FILTER'

    n_doc = "Filtering is the fundamental operation in image and video processing. Edge-preserving smoothing filters are used in many different applications."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image.")
    flags_in: bpy.props.BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")), update=update_node, subtype="NONE", description=bl_flags_list)
    sigma_s_in: bpy.props.FloatProperty(name="sigma_s_in ", default=5, min=0, max=200, update=update_node, description="Range between 0 to 200.")
    sigma_r_in: bpy.props.FloatProperty(name="sigma_r_in", default=1, min=0, max=1, step=0.01, update=update_node, description="Range between 0 to 1.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image.")

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
            'flags_in': self.get_from_props("flags_in"),
            }

        dst_out = self.process_cv(fn=cv2.edgePreservingFilter, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")
