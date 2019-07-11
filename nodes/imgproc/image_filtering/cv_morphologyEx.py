import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, MORPH_TYPE_ITEMS, BORDER_TYPE_ITEMS


class OCVLmorphologyExNode(OCVLNodeBase):

    bl_icon = 'FILTER'

    n_doc = "Performs advanced morphological transformations."
    n_requirements = {"__and__": ["src_in", "kernel_in"]}
    n_quick_link_requirements = {
        "kernel_in": {"__type_node__": "OCVLMatNode", "loc_input_mode": "MANUAL", "loc_manual_input": "[[1, 1, 1], [1, 1, 1], [1, 1, 1]]"}
    }

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Source image. The number of channels can be arbitrary. The depth should be one of CV_8U, CV_16U, CV_16S, CV_32F` or ``CV_64F.")
    kernel_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Structuring element. It can be created using getStructuringElement().")
    anchor_in: bpy.props.IntVectorProperty(default=(-1, -1), update=update_node, size=2, description="Position of the anchor within the element.")
    iterations_in: bpy.props.IntProperty(default=8, min=1, max=100, update=update_node, description="Number of times erosion is applied.")
    op_in: bpy.props.EnumProperty(items=MORPH_TYPE_ITEMS, default='MORPH_BLACKHAT', update=update_node, description="Type of a morphological operation, see cv::MorphTypes.")
    borderType_in: bpy.props.EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=update_node, description="Border mode used to extrapolate pixels outside of the image, see cv::BorderTypes")
    
    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Destination image of the same size and type as src .")

    def init(self, context):
        self.width = 200
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new("ImageSocket", "kernel_in")
        self.inputs.new('StringsSocket', "anchor_in").prop_name = 'anchor_in'
        self.inputs.new('StringsSocket', "iterations_in").prop_name = 'iterations_in'

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("src_in"),
            'kernel_in': self.get_from_props("kernel_in"),
            'anchor_in': self.get_from_props("anchor_in"),
            'iterations_in': self.get_from_props("iterations_in"),
            'op_in': self.get_from_props("op_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        dst_out = self.process_cv(fn=cv2.morphologyEx, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'op_in')
        self.add_button(layout, 'borderType_in')
