import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, NORMALIZATION_TYPE_ITEMS, COLOR_DEPTH_WITH_NONE_ITEMS


class OCVLsubtractNode(OCVLNodeBase):

    n_doc = "Calculates the per-element difference between two arrays or array and a scalar."
    n_requirements = {"__and__": ["src1_in", "src2_in"]}

    src1_in: bpy.props.StringProperty(name="src1_in", default=str(uuid.uuid4()), description="First input array or a scalar.")
    src2_in: bpy.props.StringProperty(name="src2_in", default=str(uuid.uuid4()), description="Second input array or a scalar.")
    mask_in: bpy.props.StringProperty(name="mask_in", default=str(uuid.uuid4()), description="Optional operation mask.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src1_in")
        self.inputs.new("ImageSocket", "src2_in")
        self.inputs.new('MaskSocket', "mask_in")

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src1_in': self.get_from_props("src1_in"),
            'src2_in': self.get_from_props("src2_in"),
            'mask_in': self.get_from_props("mask_in"),
            }

        if isinstance(kwargs['mask_in'], str):
            kwargs.pop('mask_in')

        dst_out = self.process_cv(fn=cv2.subtract, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
