import cv2
import bpy
import uuid

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLaddNode(OCVLNodeBase):
    n_doc = "Calculates the per-element sum of two arrays or an array and a scalar."
    n_requirements = {"__and__": ["src1", "src2"]}

    src1_in: bpy.props.StringProperty(default=str(uuid.uuid4()), update=update_node, description="First input array or a scalar.")
    src2_in: bpy.props.StringProperty(default=str(uuid.uuid4()), update=update_node, description="Second input array or a scalar.")
    mask_in: bpy.props.StringProperty(default=str(uuid.uuid4()), update=update_node, description="Optional operation mask, 8-bit single channel array, that specifies elements of the output array to be changed.")

    dst_out: bpy.props.StringProperty(default=str(uuid.uuid4()), name="Image out")

    def init(self, context):
        self.inputs.new("ImageSocket", name="src1", identifier="src1_in")
        self.inputs.new("ImageSocket", name="src2", identifier="src2_in")
        self.inputs.new('MaskSocket', name="mask", identifier="mask_in")

        self.outputs.new("ImageSocket", name="dst", identifier="dst_out")

    def wrapped_process(self):

        kwargs = {
            'src1': self.get_from_props("src1"),
            'src2': self.get_from_props("src2"),
            'mask': self.get_from_props("mask"),
            }

        if isinstance(kwargs['mask'], str):
            kwargs.pop('mask')

        dst_out = self.process_cv(fn=cv2.add, kwargs=kwargs)
        self.refresh_output_socket("dst", dst_out, is_uuid_type=True)
