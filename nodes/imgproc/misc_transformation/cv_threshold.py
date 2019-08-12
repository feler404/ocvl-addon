import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node

TYPE_THRESHOLD_ITEMS = (
    ("THRESH_BINARY", "THRESH_BINARY", "THRESH_BINARY", "", 0),
    ("THRESH_BINARY_INV", "THRESH_BINARY_INV", "THRESH_BINARY_INV", "", 1),
    ("THRESH_TRUNC", "THRESH_TRUNC", "THRESH_TRUNC", "", 2),
    ("THRESH_TOZERO", "THRESH_TOZERO", "THRESH_TOZERO", "", 3),
    ("THRESH_TOZERO_INV", "THRESH_TOZERO_INV", "THRESH_TOZERO_INV", "", 4),
    )


class OCVLthresholdNode(OCVLNodeBase):

    n_doc = "Applies a fixed-level threshold to each array element."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array (single-channel, 8-bit or 32-bit floating point).")
    thresh_in: bpy.props.IntProperty(default=127, min=0, max=255, update=update_node, subtype="FACTOR", description="Threshold value.")
    maxval_in: bpy.props.IntProperty(default=255, min=0, max=255, update=update_node, subtype="FACTOR", description="Maximum value to use with the THRESH_BINARY and THRESH_BINARY_INV thresholding types")
    type_in: bpy.props.EnumProperty(items=TYPE_THRESHOLD_ITEMS, default="THRESH_BINARY", update=update_node, description="Thresholding type (see the cv::ThresholdTypes).")
    loc_invert: bpy.props.BoolProperty(default=False, update=update_node, description="Invert output mask.")

    mask_out: bpy.props.StringProperty(name="mask_out", default=str(uuid.uuid4()), description="Output mask.")
    dst_out: bpy.props.IntProperty(name="dst_out", default=0, description="Threshold value output.")

    def init(self, context):
        self.width = 200
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new('OCVLObjectSocket', "thresh_in").prop_name = 'thresh_in'
        self.inputs.new('OCVLObjectSocket', "maxval_in").prop_name = 'maxval_in'

        self.outputs.new("OCVLImageSocket", "image_out")
        self.outputs.new("OCVLObjectSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("src_in"),
            'thresh_in': self.get_from_props("thresh_in"),
            'maxval_in': self.get_from_props("maxval_in"),
            'type_in': self.get_from_props("type_in"),
            }

        retval_out, image_out = self.process_cv(fn=cv2.threshold, kwargs=kwargs)
        if self.get_from_props("loc_invert"):
            image_out = 255 - image_out
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)
        self.refresh_output_socket("retval_out", retval_out)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "type_in")
        self.add_button(layout, "loc_invert", toggle=True, icon="CLIPUV_DEHLT", text="Inverse")
