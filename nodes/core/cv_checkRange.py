import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node
from ocvl.core.settings import DBL_MAX


COMPARE_FLAG_ITEMS = (
    ("CMP_EQ", "CMP_EQ", "CMP_EQ", "", 0),
    ("CMP_GT", "CMP_GT", "CMP_GT", "", 1),
    ("CMP_GE", "CMP_GE", "CMP_GE", "", 2),
    ("CMP_LT", "CMP_LT", "CMP_LT", "", 3),
    ("CMP_LE", "CMP_LE", "CMP_LE", "", 4),
    ("CMP_NE", "CMP_NE", "CMP_NE", "", 5),
)


class OCVLcheckRangeNode(OCVLNodeBase):

    n_doc = "Checks every element of an input array for invalid values."
    n_requirements = {"__and__": ["a_in"]}

    a_in: bpy.props.StringProperty(name="a_in", default=str(uuid.uuid4()), description="Input array.")
    quiet_in: bpy.props.BoolProperty(name="quiet_in", default=True, update=update_node, description="A flag, indicating whether the functions quietly return false when the array elements are out of range or they throw an exception.")
    minVal_in: bpy.props.FloatProperty(default=30, min=-DBL_MAX, max=DBL_MAX, update=update_node, description="Inclusive lower boundary of valid values range.")
    maxVal_in: bpy.props.FloatProperty(default=150, min=-DBL_MAX, max=DBL_MAX, update=update_node, description="Exclusive upper boundary of valid values range.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array that has the same size and type as the input arrays.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "a_in")
        self.inputs.new("OCVLObjectSocket", "minVal_in").prop_name = "minVal_in"
        self.inputs.new("OCVLObjectSocket", "maxVal_in").prop_name = "maxVal_in"

        self.outputs.new("OCVLObjectSocket", "retval_out")
        self.outputs.new("OCVLObjectSocket", "pos_out")

    def wrapped_process(self):
        kwargs = {
            'a_in': self.get_from_props("a_in"),
            'quiet_in': self.get_from_props("quiet_in"),
            'minVal_in': self.get_from_props("minVal_in"),
            'maxVal_in': self.get_from_props("maxVal_in"),
            }

        retval_out, pos_out = self.process_cv(fn=cv2.checkRange, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)
        self.refresh_output_socket("pos_out", pos_out, is_uuid_type=True)
