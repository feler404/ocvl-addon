import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, NORMALIZATION_TYPE_ITEMS, COLOR_DEPTH_WITH_NONE_ITEMS


class OCVLnormNode(OCVLNodeBase):

    n_doc = "Calculates an absolute array norm, an absolute difference norm, or a relative difference norm."
    n_requirements = {"__and__": ["src1_in"]}

    src1_in: bpy.props.StringProperty(name="src1_in", default=str(uuid.uuid4()), description="First input array or a scalar.")
    src2_in: bpy.props.StringProperty(name="src2_in", default=str(uuid.uuid4()), description="Second input array or a scalar.")
    mask_in: bpy.props.StringProperty(name="mask_in", default=str(uuid.uuid4()), description="Optional operation mask.")
    norm_type_in: bpy.props.EnumProperty(items=NORMALIZATION_TYPE_ITEMS, default="NORMAL_CLONE", update=update_node, description="Normalization type (see cv::NormTypes).")

    retval_out: bpy.props.StringProperty(name="retval_out", default=str(uuid.uuid4()), description="Output array.")

    def init(self, context):
        self.width = 200
        self.inputs.new("OCVLImageSocket", "src1_in")
        self.inputs.new("OCVLImageSocket", "src2_in")
        self.inputs.new('OCVLMaskSocket', "mask_in")

        self.outputs.new("OCVLObjectSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'src1_in': self.get_from_props("src1_in"),
            'src2_in': self.get_from_props("src2_in"),
            'mask_in': self.get_from_props("mask_in"),
            }

        retval_out = self.process_cv(fn=cv2.norm, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "norm_type_in")
