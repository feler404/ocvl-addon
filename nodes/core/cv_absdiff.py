import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLabsdifflalamidoNode(OCVLNodeBase):
    n_doc = "Calculates the per-element absolute difference between two arrays or between an array and a scalar."
    n_note = "Saturation is not applied when the arrays have the depth CV_32S. You may even get a negative value in the case of overflow."
    n_see_also = "abs"
    n_requirements = {"__and__": ["src1_in", "src2_in"]}

    src1_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="First input array or a scalar.")
    src2_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="Second input array or a scalar.")

    dst_out: bpy.props.StringProperty(default=str(uuid.uuid4()), description="Output array that has the same size and type as input arrays.")

    def init(self, context):
        self.inputs.new("ImageSocket", name="src1_in", identifier="src1_in")
        self.inputs.new("ImageSocket", name="src2_in", identifier="src2_in")

        self.outputs.new("ImageSocket", name="dst_out", identifier="dst_out")

    def wrapped_process(self):
        kwargs = {
            'src1': self.get_from_props("src1_in"),
            'src2': self.get_from_props("src2_in"),
            }

        dst_out = self.process_cv(fn=cv2.absdiff, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass
