import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLsolvePolyNode(OCVLNodeBase):

    n_doc = "Finds the real or complex roots of a polynomial equation."
    n_requirements = {"__and__": ["coeffs_in"]}
    n_quick_link_requirements = {"coeffs_in": {"loc_input_mode": "MANUAL", "value_type_in": "float32", "loc_manual_input": "[1, 2, 3, 4, 5]"}}

    coeffs_in: bpy.props.StringProperty(name="coeffs_in", default=str(uuid.uuid4()),  description="Array of polynomial coefficients.")
    maxIters_in: bpy.props.IntProperty(name="maxIters_in", default=300, min=1, max=3000, update=update_node, description="Maximum number of iterations the algorithm does.")

    retval_out: bpy.props.StringProperty(name="retval_out", default=str(uuid.uuid4()), description="Output solution.")
    roots_out: bpy.props.StringProperty(name="roots_out", default=str(uuid.uuid4()), description="Output solution.")

    def init(self, context):
        self.inputs.new("OCVLVectorSocket", "coeffs_in")
        self.inputs.new("OCVLMatrixSocket", "maxIters_in").prop_name = "maxIters_in"

        self.outputs.new("OCVLMatrixSocket", "retval_out")
        self.outputs.new("OCVLMatrixSocket", "roots_out")

    def wrapped_process(self):
        kwargs = {
            'coeffs_in': self.get_from_props("coeffs_in"),
            'maxIters_in': self.get_from_props("maxIters_in"),
            }

        retval_out, roots_out = self.process_cv(fn=cv2.solvePoly, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)
        self.refresh_output_socket("roots_out", roots_out, is_uuid_type=True)
