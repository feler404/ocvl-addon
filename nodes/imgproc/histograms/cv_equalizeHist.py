import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLequalizeHistNode(OCVLNodeBase):

    n_doc = "Equalizes the histogram of a grayscale image."
    n_quick_link_requirements = {"src_in": {"code_in": "COLOR_BGR2GRAY"}}
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Source 8-bit single channel image.")
    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("src_in"),
        }

        dst_out = self.process_cv(fn=cv2.equalizeHist, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
