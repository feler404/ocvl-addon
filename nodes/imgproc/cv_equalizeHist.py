import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLequalizeHistNode(OCVLNodeBase):

    n_doc = "Equalizes the histogram of a grayscale image."
    n_quick_link_requirements = {"image_in": {"code_in": "COLOR_BGR2GRAY"}}
    n_requirements = {"__and__": ["image_in"]}

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()), description="Source 8-bit single channel image.")
    image_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.inputs.new("ImageSocket", "image_in")
        self.outputs.new("ImageSocket", "image_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("image_in"),
        }

        image_out = self.process_cv(fn=cv2.equalizeHist, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)
