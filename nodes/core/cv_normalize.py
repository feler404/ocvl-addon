import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, NORMALIZATION_TYPE_ITEMS, COLOR_DEPTH_WITH_NONE_ITEMS


class OCVLnormalizeNode(OCVLNodeBase):

    n_doc = "Normalizes the norm or value range of an array."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array.")
    mask_in: bpy.props.StringProperty(name="mask_in", default=str(uuid.uuid4()), description="Optional operation mask.")
    alpha_in: bpy.props.FloatProperty(default=150, min=0.0, max=1000, update=update_node, description="Norm value to normalize to or the lower range boundary in case of the range normalization.")
    beta_in: bpy.props.FloatProperty(default=255, min=0.0, max=1000, update=update_node, description="Upper range boundary in case of the range normalization; it is not used for the norm normalization.")
    norm_type_in: bpy.props.EnumProperty(items=NORMALIZATION_TYPE_ITEMS, default="NORMAL_CLONE", update=update_node, description="Normalization type (see cv::NormTypes).")
    dtype_in: bpy.props.EnumProperty(items=COLOR_DEPTH_WITH_NONE_ITEMS, default='None', update=update_node, description="Channels as src and the depth =CV_MAT_DEPTH(dtype).")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array.")

    def init(self, context):
        self.width = 200
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new('MaskSocket', "mask_in")
        self.inputs.new('StringsSocket', "alpha_in").prop_name = 'alpha_in'
        self.inputs.new('StringsSocket', "beta_in").prop_name = 'beta_in'

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        src_in = self.get_from_props("src_in")
        dst = src_in.copy()
        dtype_in = self.get_from_props("dtype_in")
        dtype_in = -1 if dtype_in is None else dtype_in
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'mask_in': self.get_from_props("mask_in"),
            'dst': dst,
            'alpha_in': self.get_from_props("alpha_in"),
            'beta_in': self.get_from_props("beta_in"),
            'norm_type_in': self.get_from_props("norm_type_in"),
            'dtype_in': dtype_in
            }

        dst_out = self.process_cv(fn=cv2.normalize, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "norm_type_in")
        self.add_button(layout, "dtype_in", expand=True)
