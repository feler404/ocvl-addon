import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLinvertAffineTransformNode(OCVLNodeBase):

    n_doc = "Inverts an affine transformation."
    n_requirements = {"__and__": ["M_in"]}
    n_quick_link_requirements = {
        "M_in": {"__type_node__": "OCVLMatNode", "loc_input_mode": "MANUAL", "loc_manual_input": "[[1,0,100],[0,1,50]]", "value_type_in": "float32"}
    }

    M_in: bpy.props.StringProperty(name="M_in", default=str(uuid.uuid4()), description="Original affine transformation.")
    iM_out: bpy.props.StringProperty(name="iM_out", default=str(uuid.uuid4()), description="Output reverse affine transformation.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "M_in")
        self.outputs.new("OCVLMatrixSocket", "iM_out")

    def wrapped_process(self):
        kwargs = {
            'M_in': self.get_from_props("M_in"),
            }

        iM_out = self.process_cv(fn=cv2.invertAffineTransform, kwargs=kwargs)
        self.refresh_output_socket("iM_out", iM_out, is_uuid_type=True)

