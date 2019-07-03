import cv2
import uuid
import bpy

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLbitwise_orNode(OCVLNodeBase):
    n_doc = "Calculates the per-element bit-wise disjunction of two arrays or an array and a scalar."
    n_requirements = {"__and__": ["src1_in", "src2_in"]}

    src1_in: bpy.props.StringProperty(name="src1_in", update=update_node, default=str(uuid.uuid4()), description="First input array or a scalar.")
    src2_in: bpy.props.StringProperty(name="src2_in", update=update_node, default=str(uuid.uuid4()), description="Second input array or a scalar.")
    mask_in: bpy.props.StringProperty(name="mask_in", update=update_node, default=str(uuid.uuid4()), description="Optional operation mask, 8-bit single channel array, that specifies elements of the output array to be changed.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()))

    def init(self, context):
        self.inputs.new("ImageSocket", name="src1_in", identifier="src1_in")
        self.inputs.new("ImageSocket", name="src2_in", identifier="src2_in")
        self.inputs.new('MaskSocket', name="mask_in", identifier="mask_in")

        self.outputs.new("ImageSocket", name="dst_out", identifier="dst_out")

    def wrapped_process(self):
        kwargs = {
            'src1_in': self.get_from_props("src1_in"),
            'src2_in': self.get_from_props("src2_in"),
            'mask_in': self.get_from_props("mask_in"),
            }

        dst_out = self.process_cv(fn=cv2.bitwise_or, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
