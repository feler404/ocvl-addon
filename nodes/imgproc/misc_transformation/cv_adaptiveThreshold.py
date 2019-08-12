import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, TYPE_THRESHOLD_ITEMS

ADAPTIVE_METHOD_ITEMS = (
    ("ADAPTIVE_THRESH_GAUSSIAN_C", "ADAPTIVE_THRESH_GAUSSIAN_C", "ADAPTIVE_THRESH_GAUSSIAN_C", "", 0),
    ("ADAPTIVE_THRESH_MEAN_C", "ADAPTIVE_THRESH_MEAN_C", "ADAPTIVE_THRESH_MEAN_C", "", 1),
)

KERNEL_SIZE_ITEMS = (
    ("3", "3", "3", "", 0),
    ("5", "5", "5", "", 1),
    ("7", "7", "7", "", 2),
)


class OCVLadaptiveThresholdNode(OCVLNodeBase):

    bl_icon = 'MOD_MASK'

    n_doc = "Applies an adaptive threshold to an array."
    n_quick_link_requirements = {"image_in": {"code_in": "COLOR_BGR2GRAY"}}
    n_requirements = {"__and__": ["image_in"]}

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()), description="Source 8-bit single-channel image.")
    maxValue_in: bpy.props.IntProperty(default=150, min=0, max=255, update=update_node, description="Non-zero value assigned to the pixels for which the condition is satisfied.")
    adaptiveMethod_in: bpy.props.EnumProperty(items=ADAPTIVE_METHOD_ITEMS, default="ADAPTIVE_THRESH_MEAN_C", update=update_node, description="Adaptive thresholding algorithm to use, see cv::AdaptiveThresholdTypes .")
    thresholdType_in: bpy.props.EnumProperty(items=TYPE_THRESHOLD_ITEMS, default="THRESH_BINARY", update=update_node, description="Thresholding type that must be either THRESH_BINARY or THRESH_BINARY_INV, etc.")
    blockSize_in: bpy.props.EnumProperty(items=KERNEL_SIZE_ITEMS, default="3", update=update_node, description="Size of a pixel neighborhood that is used to calculate a threshold value for the pixel.")
    C_in: bpy.props.FloatProperty(default=15, min=0, max=200, step=20, update=update_node, description="Constant subtracted from the mean or weighted mean.")

    image_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()), description="Destination image of the same size and the same type as src.")

    def init(self, context):
        self.width = 250
        self.inputs.new("OCVLImageSocket", "image_in")
        self.inputs.new("OCVLObjectSocket", "maxValue_in").prop_name = "maxValue_in"
        self.inputs.new("OCVLObjectSocket", "C_in").prop_name = "C_in"

        self.outputs.new("OCVLImageSocket", "image_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("image_in"),
            'maxValue_in': self.get_from_props("maxValue_in"),
            'adaptiveMethod_in': self.get_from_props("adaptiveMethod_in"),
            'thresholdType_in': self.get_from_props("thresholdType_in"),
            'blockSize_in': int(self.get_from_props("blockSize_in")),
            'C_in': self.get_from_props("C_in"),
            }

        image_out = self.process_cv(fn=cv2.adaptiveThreshold, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout=layout, prop_name="adaptiveMethod_in", expand=True)
        self.add_button(layout=layout, prop_name="thresholdType_in")
        self.add_button(layout=layout, prop_name="blockSize_in", expand=True)
