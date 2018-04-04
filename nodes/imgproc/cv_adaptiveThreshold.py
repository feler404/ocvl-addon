import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatProperty

from ...extend.utils import cv_register_class, cv_unregister_class, TYPE_THRESHOLD_ITEMS, OCVLNode, updateNode


ADAPTIVE_METHOD_ITEMS = (
    ("ADAPTIVE_THRESH_GAUSSIAN_C", "ADAPTIVE_THRESH_GAUSSIAN_C", "ADAPTIVE_THRESH_GAUSSIAN_C", "", 0),
    ("ADAPTIVE_THRESH_MEAN_C", "ADAPTIVE_THRESH_MEAN_C", "ADAPTIVE_THRESH_MEAN_C", "", 1),
)

KERNEL_SIZE_ITEMS = (
    ("3", "3", "3", "", 0),
    ("5", "5", "5", "", 1),
    ("7", "7", "7", "", 2),
)


class OCVLadaptiveThresholdNode(OCVLNode):

    bl_icon = 'MOD_MASK'

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description="Source 8-bit single-channel image.")
    maxValue_in = IntProperty(default=150, min=0, max=255, update=updateNode,
        description="Non-zero value assigned to the pixels for which the condition is satisfied.")
    adaptiveMethod_in = EnumProperty(items=ADAPTIVE_METHOD_ITEMS, default="ADAPTIVE_THRESH_MEAN_C", update=updateNode,
        description="Adaptive thresholding algorithm to use, see cv::AdaptiveThresholdTypes .")
    thresholdType_in = EnumProperty(items=TYPE_THRESHOLD_ITEMS, default="THRESH_BINARY", update=updateNode,
        description="Thresholding type that must be either THRESH_BINARY or THRESH_BINARY_INV, etc.")
    blockSize_in = EnumProperty(items=KERNEL_SIZE_ITEMS, default="3", update=updateNode,
        description="Size of a pixel neighborhood that is used to calculate a threshold value for the pixel.")
    C_in = FloatProperty(default=15, min=0, max=200, step=20, update=updateNode,
        description="Constant subtracted from the mean or weighted mean.")

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description="Destination image of the same size and the same type as src.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "maxValue_in").prop_name = "maxValue_in"
        self.inputs.new("StringsSocket", "C_in").prop_name = "C_in"

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

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


def register():
    cv_register_class(OCVLadaptiveThresholdNode)


def unregister():
    cv_unregister_class(OCVLadaptiveThresholdNode)
