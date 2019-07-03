import cv2
import bpy
import uuid

from ocvl.core.node_base import OCVLNodeBase, COLOR_DEPTH_WITH_NONE_ITEMS, update_node


class OCVLaddNode(OCVLNodeBase):
    n_doc = "Calculates the per-element sum of two arrays or an array and a scalar."
    n_requirements = {"__and__": ["src1_in", "src2_in"]}

    src1_in: bpy.props.StringProperty(default=str(uuid.uuid4()), update=update_node, description="First input array or a scalar.")
    src2_in: bpy.props.StringProperty(default=str(uuid.uuid4()), update=update_node, description="Second input array or a scalar.")
    mask_in: bpy.props.StringProperty(default=str(uuid.uuid4()), update=update_node, description="Optional operation mask, 8-bit single channel array, that specifies elements of the output array to be changed.")
    dtype_in: bpy.props.EnumProperty(items=COLOR_DEPTH_WITH_NONE_ITEMS, default='None', update=update_node, description="Optional depth of the output array.")

    dst_out: bpy.props.StringProperty(default=str(uuid.uuid4()), name="dst_out")

    def init(self, context):
        self.inputs.new("ImageSocket", name="src1_in", identifier="src1_in")
        self.inputs.new("ImageSocket", name="src2_in", identifier="src2_in")
        self.inputs.new('MaskSocket', name="mask_in", identifier="mask_in")

        self.outputs.new("ImageSocket", name="dst_out", identifier="dst_out")

    def wrapped_process(self):
        dtype_in = self.get_from_props("dtype_in")

        kwargs = {
            'src1_in': self.get_from_props("src1_in"),
            'src2_in': self.get_from_props("src2_in"),
            'mask_in': self.get_from_props("mask_in"),
            'dtype_in': -1 if dtype_in is None else dtype_in
            }

        dst_out = self.process_cv(fn=cv2.add, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "dtype_in", expand=True)