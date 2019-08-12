import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, BORDER_TYPE_ITEMS


class OCVLcornerHarrisNode(OCVLNodeBase):

    n_doc = "Harris corner detector."
    n_quick_link_requirements = {"src_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32", "color_in": (0, 0, 0, 0)}}
    n_requirements = {"__and__": ["src_in"]}

    def set_ksize(self, value):
        if value % 2 == 0:
            value = value + 1
        self["ksize_in"] = value

    def get_ksize(self):
        return self.get("ksize_in", 1)

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input single-channel 8-bit or floating-point image.")
    blockSize_in: bpy.props.IntProperty(default=2, min=1, max=30, update=update_node, description="Neighborhood size (see the details on cornerEigenValsAndVecs ).")
    ksize_in: bpy.props.IntProperty(default=3, min=1, max=30, step=2, set=set_ksize, get=get_ksize, update=update_node, description="Aperture parameter for the Sobel operator.")
    k_in: bpy.props.FloatProperty(default=0.04, min=0.01, max=1, update=update_node, description="Harris detector free parameter. See the formula below.")
    borderType_in: bpy.props.EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=update_node, description="Pixel extrapolation method. See cv::BorderTypes.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Image to store the Harris detector responses.")

    def init(self, context):

        self.width = 150
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new('OCVLMatrixSocket', "blockSize_in").prop_name = 'blockSize_in'
        self.inputs.new('OCVLMatrixSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('OCVLMatrixSocket', "k_in").prop_name = 'k_in'

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):

        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'blockSize_in': self.get_from_props("blockSize_in"),
            'ksize_in': self.get_from_props("ksize_in"),
            'k_in': self.get_from_props("k_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        dst_out = self.process_cv(fn=cv2.cornerHarris, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')
