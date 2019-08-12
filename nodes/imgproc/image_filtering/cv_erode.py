import uuid

import bpy
import cv2
import numpy as np
from ocvl.core.node_base import OCVLNodeBase, update_node, BORDER_TYPE_ITEMS


class OCVLerodeNode(OCVLNodeBase):

    bl_icon = 'FILTER'

    n_doc = "Erodes an image by using a specific structuring element."
    n_requirements = {"__and__": ["src_in", "kernel_in"]}
    n_quick_link_requirements = {
        "kernel_in": {"__type_node__": "OCVLMatNode", "loc_input_mode": "MANUAL", "loc_manual_input": "[[1, 1, 1], [1, 1, 1], [1, 1, 1]]"}
    }

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image.")
    kernel_in: bpy.props.StringProperty(name="kernel_in", default=str(uuid.uuid4()), description="Structuring element used for dilation.")
    anchor_in: bpy.props.IntVectorProperty(default=(-1, -1), update=update_node, size=2, description="Position of the anchor within the element.")
    iterations_in: bpy.props.IntProperty(default=2, min=1, max=10, update=update_node, description="Number of times erosion is applied.")
    borderType_in: bpy.props.EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=update_node, description="border mode used to extrapolate pixels outside of the image, see cv::BorderTypes")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.width = 150
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLImageSocket", "kernel_in")
        self.inputs.new('OCVLMatrixSocket', "anchor_in").prop_name = 'anchor_in'
        self.inputs.new('OCVLMatrixSocket', "iterations_in").prop_name = 'iterations_in'

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("src_in"),
            'kernel_in': self.get_from_props("kernel_in"),
            'anchor_in': self.get_from_props("anchor_in"),
            'iterations_in': self.get_from_props("iterations_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        dst_out = self.process_cv(fn=cv2.erode, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')
