import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLdecolorNode(OCVLNodeBase):

    n_doc = "Transforms a color image to a grayscale image. It is a basic tool in digital printing, stylized black-and-white photograph rendering, and in many single channel image processing applications"
    n_requirements = {"__and__": ["src_in",]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input 8-bit 3-channel image.")

    grayscale_out: bpy.props.StringProperty(name="grayscale_out", default=str(uuid.uuid4()), description="Output 8-bit 1-channel image..")
    color_boost_out: bpy.props.StringProperty(name="color_boost_out", default=str(uuid.uuid4()), description="Output 8-bit 3-channel image.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")

        self.outputs.new("OCVLObjectSocket", "grayscale_out")
        self.outputs.new("OCVLObjectSocket", "color_boost_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': [self.get_from_props("src_in")],
        }

        grayscale_out, color_boost_out = self.process_cv(fn=cv2.decolor, kwargs=kwargs)
        self.refresh_output_socket("grayscale_out", grayscale_out, is_uuid_type=True),
        self.refresh_output_socket("color_boost_out", color_boost_out, is_uuid_type=True),
