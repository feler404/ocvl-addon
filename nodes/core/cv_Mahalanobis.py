import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLMahalanobisNode(OCVLNodeBase):

    n_doc = "Calculates the Mahalanobis distance between two vectors."
    n_requirements = {"__and__": ["v1_in", "v2_in", "icovar_in"]}
    n_quick_link_requirements = {
        "v1_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32", "width_in": 10, "height_in": 10},
        "v2_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32", "width_in": 10, "height_in": 10},
        "icovar_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
    }

    v1_in: bpy.props.StringProperty(name="v1_in", default=str(uuid.uuid4()), description="First 1D input vector.")
    v2_in: bpy.props.StringProperty(name="v2_in", default=str(uuid.uuid4()), description="Second 1D input vector.")
    icovar_in: bpy.props.StringProperty(name="icovar_in", default=str(uuid.uuid4()), description="Inverse covariance matrix.")

    retval_out: bpy.props.FloatProperty(name="retval_out", description="Return value.")

    def init(self, context):
        self.inputs.new("ImageSocket", "v1_in")
        self.inputs.new("ImageSocket", "v2_in")
        self.inputs.new("ImageSocket", "icovar_in")

        self.outputs.new("StringsSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'v1_in': self.get_from_props("v1_in"),
            'v2_in': self.get_from_props("v2_in"),
            'icovar_in': self.get_from_props("icovar_in"),
            }

        retval_out = self.process_cv(fn=cv2.Mahalanobis, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out)
