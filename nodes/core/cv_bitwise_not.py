import cv2
import uuid
import bpy

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLbitwise_notNode(OCVLNodeBase):
    n_doc = "Inverts every bit of an array."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(default=str(uuid.uuid4()), update=update_node, description="First input array or a scalar.")
    mask_in: bpy.props.StringProperty(default=str(uuid.uuid4()), update=update_node, description="Optional operation mask, 8-bit single channel array, that specifies elements of the output array to be changed.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()))

    def init(self, context):
        self.inputs.new("OCVLImageSocket", name="src_in", identifier="src_in")
        self.inputs.new('OCVLMaskSocket', name="mask_in", identifier="mask_in")

        self.outputs.new("OCVLImageSocket", name="dst_out", identifier="dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'mask_in': self.get_from_props("mask_in"),
            }

        dst_out = self.process_cv(fn=cv2.bitwise_not, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
