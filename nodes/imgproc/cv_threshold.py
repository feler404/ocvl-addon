import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, IntProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


TYPE_THRESHOLD_ITEMS = (
    ("THRESH_BINARY", "THRESH_BINARY", "THRESH_BINARY", "", 0),
    ("THRESH_BINARY_INV", "THRESH_BINARY_INV", "THRESH_BINARY_INV", "", 1),
    ("THRESH_TRUNC", "THRESH_TRUNC", "THRESH_TRUNC", "", 2),
    ("THRESH_TOZERO", "THRESH_TOZERO", "THRESH_TOZERO", "", 3),
    ("THRESH_TOZERO_INV", "THRESH_TOZERO_INV", "THRESH_TOZERO_INV", "", 4),
    )


class OCVLthresholdNode(OCVLNode):
    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))
    retval_out = IntProperty(name="retval_out", default=0)

    thresh_in = IntProperty(default=127, min=0, max=255, update=updateNode,
        description="Threshold value.")
    maxval_in = IntProperty(default=255, min=0, max=255, update=updateNode,
        description="Maximum value to use with the THRESH_BINARY and THRESH_BINARY_INV thresholding types")
    type_in = EnumProperty(items=TYPE_THRESHOLD_ITEMS, default="THRESH_BINARY", update=updateNode,
        description="Thresholding type (see the cv::ThresholdTypes).")
    loc_invert = BoolProperty(default=False, update=updateNode,
        description="Invert output mask.")

    def sv_init(self, context):
        self.width = 200
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "thresh_in").prop_name = 'thresh_in'
        self.inputs.new('StringsSocket', "maxval_in").prop_name = 'maxval_in'

        self.outputs.new("StringsSocket", "image_out")
        self.outputs.new("StringsSocket", "retval_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
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


def register():
    cv_register_class(OCVLthresholdNode)


def unregister():
    cv_unregister_class(OCVLthresholdNode)
