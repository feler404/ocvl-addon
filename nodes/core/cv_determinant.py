import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLdeterminantNode(OCVLNodeBase):

    n_doc = "Returns the determinant of a square floating-point matrix."
    n_requirements = {"__and__": ["mtx_in"]}
    n_quick_link_requirements = {"mtx_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"}}

    mtx_in: bpy.props.StringProperty(name="mtx_in", default=str(uuid.uuid4()), description="Input matrix that must have CV_32FC1 or CV_64FC1 type and square size.")
    retval_out: bpy.props.FloatProperty(name="retval_out", description="")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "mtx_in")
        self.outputs.new("OCVLMatrixSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'mtx_in': self.get_from_props("mtx_in"),
            }

        retval_out = self.process_cv(fn=cv2.determinant, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out)
