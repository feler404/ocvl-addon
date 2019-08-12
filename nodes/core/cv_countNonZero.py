import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLcountNonZeroNode(OCVLNodeBase):

    n_doc = "Counts non-zero array elements."
    n_requirements = {"__and__": ["src_in"]}
    n_quick_link_requirements = {"src_in": {"code_in": "COLOR_BGR2GRAY", "color_in": (0, 0, 0, 0)}}

    src_in: bpy.props.StringProperty(name="src", default=str(uuid.uuid4()), description="First input single channel array or a scalar.")
    retval_out: bpy.props.IntProperty(name="retval", default=0, description="")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.outputs.new("OCVLMatrixSocket", "retval_out").prop_name = "retval_out"

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            }

        self.retval_out = self.process_cv(fn=cv2.countNonZero, kwargs=kwargs)
        self.refresh_output_socket("retval_out", self.retval_out)

    def draw_buttons(self, context, layout):
        layout.label(text=str(self.retval_out))