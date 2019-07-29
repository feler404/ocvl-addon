import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, BORDER_TYPE_ITEMS

class OCVLmedianBlurNode(OCVLNodeBase):
    n_doc = "Blurs an image using the normalized box filter."
    n_see_also = "bileteralFilter,blur,boxFilter,GaussianBlur"
    n_requirements = {"__and__": ["src_in"]}

    def set_ksize(self, value):
        if value % 2 == 0:
            value = value + 1
        self["ksize_in"] = value

    def get_ksize(self):
        return self.get("ksize_in", 5)

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image.")
    ksize_in: bpy.props.IntProperty(default=5, update=update_node, min=1, max=30, get=get_ksize, set=set_ksize,description="Aperture linear size; it must be odd and greater than 1, for example: 3, 5, 7 ...")

    dst_in: bpy.props.StringProperty(name="dst_in", default=str(uuid.uuid4()),description="Destination array of the same size and type as src.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'

        self.outputs.new("ImageSocket", "dst_in")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("src_in"),
            'ksize_in': self.get_from_props("ksize_in"),
        }

        dst_in = self.process_cv(fn=cv2.medianBlur, kwargs=kwargs)
        self.refresh_output_socket("dst_in", dst_in, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')