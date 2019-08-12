import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLeigenNode(OCVLNodeBase):

    n_doc = "Calculates eigenvalues and eigenvectors of a symmetric matrix."
    n_requirements = {"__and__": ["src_in"]}
    n_quick_link_requirements = {"src_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"}}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input matrix that must have CV_32FC1 or CV_64FC1 type, square size and be symmetrical.")

    retval_out: bpy.props.StringProperty(name="retval_out", default=str(uuid.uuid4()), description="Return value.")
    eigenvalues_out: bpy.props.StringProperty(name="eigenvalues_out", default=str(uuid.uuid4()), description="Output vector of eigenvalues of the same type as src; the eigenvalues are stored in the descending order.")
    eigenvectors_out: bpy.props.StringProperty(name="eigenvectors_out", default=str(uuid.uuid4()), description="Output matrix of eigenvectors; it has the same size and type as src.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")

        self.outputs.new("OCVLObjectSocket", "retval_out")
        self.outputs.new("OCVLObjectSocket", "eigenvalues_out")
        self.outputs.new("OCVLObjectSocket", "eigenvectors_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            }

        retval_out, eigenvalues_out, eigenvectors_out = self.process_cv(fn=cv2.eigen, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)
        self.refresh_output_socket("eigenvalues_out", eigenvalues_out, is_uuid_type=True)
        self.refresh_output_socket("eigenvectors_out", eigenvectors_out, is_uuid_type=True)
