import uuid
import cv2
import bpy
import numpy as np

from ocvl.core.node_base import OCVLNodeBase, update_node, COLOR_DEPTH_ITEMS, BORDER_TYPE_ITEMS


class OCVLfilter2dNode(OCVLNodeBase):
    bl_icon = 'FILTER'

    n_doc = "Convolves an image with the kernel."
    n_requirements = {"__and__": ["src_in", "kernel_in"]}
    n_quick_link_requirements = {
        "kernel_in": {"__type_node__": "OCVLMatNode", "loc_input_mode": "MANUAL", "loc_manual_input": "[[1, 1, 0], [1, 0, 0], [0, 0, 0]]"}
    }

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image.")
    ddepth_in: bpy.props.EnumProperty(items=COLOR_DEPTH_ITEMS, default='CV_8U', update=update_node, description="Desired depth of the destination image, see @ref filter_depths 'combinations'")
    anchor_in: bpy.props.IntVectorProperty(default=(-1, -1), update=update_node, size=2, description="Anchor of the kernel that indicates the relative position of a filtered point within the kernel; the anchor should lie within the kernel; default value (-1,-1) means that the anchor is at the kernel center.")
    delta_in: bpy.props.IntProperty(default=0, update=update_node, min=0, max=255, description="Optional value added to the filtered pixels before storing them in dst.")
    borderType_in: bpy.props.EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=update_node, description="Pixel extrapolation method, see cv::BorderTypes")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.width = 250
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLImageSocket", "kernel_in")
        self.inputs.new('OCVLObjectSocket', "anchor_in").prop_name = 'anchor_in'
        self.inputs.new('OCVLObjectSocket', "delta_in").prop_name = 'delta_in'

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("src_in"),
            'ddepth_in': self.get_from_props("ddepth_in"),
            'delta_in': self.get_from_props("delta_in"),
            'kernel_in': self.get_from_props("kernel_in"),
            'anchor_in': self.get_from_props("anchor_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        dst_out = self.process_cv(fn=cv2.filter2D, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'ddepth_in')
        self.add_button(layout, 'borderType_in')
