import cv2
import uuid
import bpy

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLbitwise_andNode(OCVLNodeBase):

    n_doc = "Computes bitwise conjunction of the two arrays (dst = src1 & src2) Calculates the per-element bit-wise conjunction of two arrays or an array and a scalar."
    n_requirements = {"__and__": ["src1_in", "src2_in"]}

    src1_in: bpy.props.StringProperty(name="src1_in", default=str(uuid.uuid4()), update=update_node, description="First input array or a scalar.")
    src2_in: bpy.props.StringProperty(name="src2_in", default=str(uuid.uuid4()), update=update_node, description="Second input array or a scalar.")
    mask_in: bpy.props.StringProperty(name="mask_in", default=str(uuid.uuid4()), update=update_node, description="Optional operation mask, 8-bit single channel array, that specifies elements of the output array to be changed.")

    dst_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()))

    def init(self, context):
        self.inputs.new("ImageSocket", name="src1_in", identifier="src1_in")
        self.inputs.new("ImageSocket", name="src2_in", identifier="src2_in")
        self.inputs.new('MaskSocket', name="mask_in", identifier="mask_in")

        self.outputs.new("ImageSocket", name="dst_out", identifier="dst_out")

    def wrapped_process(self):
        kwargs = {
            'src1': self.get_from_props("src1_in"),
            'src2': self.get_from_props("src2_in"),
            'mask': self.get_from_props("mask_in"),
            }

        if isinstance(kwargs['mask'], str):
            kwargs.pop('mask')

        dst_out = self.process_cv(fn=cv2.bitwise_and, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
