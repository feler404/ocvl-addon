import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node, REDUCE_TYPES_ITEMS


class OCVLsolveCubicNode(OCVLNodeBase):

    n_doc = "Finds the real roots of a cubic equation."
    n_requirements = {"__and__": ["coeffs_in"]}
    n_quick_link_requirements = {"coeffs_in": {"loc_input_mode": "MANUAL", "value_type_in": "float32", "loc_manual_input": "[1, 2, 3]"}}

    coeffs_in: bpy.props.StringProperty(name="coeffs_in", default=str(uuid.uuid4()),  description="Equation coefficients, an array of 3 or 4 elements.")

    retval_out: bpy.props.StringProperty(name="retval_out", default=str(uuid.uuid4()), description="Output solution.")
    roots_out: bpy.props.StringProperty(name="roots_out", default=str(uuid.uuid4()), description="Output solution.")

    def init(self, context):
        self.inputs.new("VectorSocket", "coeffs_in")

        self.outputs.new("StringsSocket", "retval_out")
        self.outputs.new("StringsSocket", "roots_out")

    def wrapped_process(self):
        kwargs = {
            'coeffs_in': self.get_from_props("coeffs_in"),
            }

        retval_out, roots_out = self.process_cv(fn=cv2.solveCubic, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)
        self.refresh_output_socket("roots_out", roots_out, is_uuid_type=True)
