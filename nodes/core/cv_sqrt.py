import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase


class OCVLsqrtNode(OCVLNodeBase):

    n_doc = "Calculates a square root of array elements."
    n_requirements = {"__and__": ["src_in"]}
    n_quick_link_requirements = {"src_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"}}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input floating-point array.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same size and type as src1.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.outputs.new("StringsSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            }

        dst_out = self.process_cv(fn=cv2.sqrt, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
