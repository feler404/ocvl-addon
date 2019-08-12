import cv2
import uuid

import bpy
import numpy as np
from ocvl.core.node_base import OCVLNodeBase, update_node
from ocvl.core.exceptions import IncorrectTypeInStringSocketException
from ocvl.core.constants import MAP_NUMPY_CTYPES_OPENCV_CTYPES


COMPARE_FLAG_ITEMS = (
    ("CMP_EQ", "CMP_EQ", "CMP_EQ", "", 0),
    ("CMP_GT", "CMP_GT", "CMP_GT", "", 1),
    ("CMP_GE", "CMP_GE", "CMP_GE", "", 2),
    ("CMP_LT", "CMP_LT", "CMP_LT", "", 3),
    ("CMP_LE", "CMP_LE", "CMP_LE", "", 4),
    ("CMP_NE", "CMP_NE", "CMP_NE", "", 5),
)


class OCVLcalcCovarMatrixNode(OCVLNodeBase):

    bl_flags_list = 'COVAR_SCRAMBLED, COVAR_NORMAL, COVAR_USE_AVG, COVAR_SCALE, COVAR_ROWS, COVAR_COLS'
    _bl_flags_list_default_values = [False, False, False, False, False, True]

    n_doc = "Calculates the covariance matrix of a set of vectors."
    n_quick_link_requirements = {"samples_in": {"width_in": 30, "height_in": 30, "code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"}}
    n_requirements = {"__and__": ["samples_in"]}

    samples_in: bpy.props.StringProperty(name="samples_in", default=str(uuid.uuid4()), description="Samples stored either as separate matrices or as rows/columns of a single matrix.")
    mean_in: bpy.props.IntProperty(name="mean_in", default=10, update=update_node, description="Input or output (depending on the flags) array as the average value of the input vectors.")
    flags_in: bpy.props.BoolVectorProperty(default=_bl_flags_list_default_values, update=update_node, size=len(bl_flags_list.split(",")), subtype="NONE", description=bl_flags_list)

    covar_out: bpy.props.StringProperty(name="covar_out", default=str(uuid.uuid4()), description="Output covariance matrix of the type ctype and square size.")
    mean_out: bpy.props.StringProperty(name="mean_out", default=str(uuid.uuid4()), description="Output (depending on the flags) array as the average value of the input vectors.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "samples_in")
        self.inputs.new("OCVLMatrixSocket", "mean_in").prop_name = "mean_in"

        self.outputs.new("OCVLMatrixSocket", "covar_out")
        self.outputs.new("OCVLMatrixSocket", "mean_out")

    def wrapped_process(self):
        kwargs = {
            'samples_in': self.get_from_props("samples_in"),
            'flags_in': self.get_from_props("flags_in"),
            'mean_in': self.get_from_props("mean_in"),
            }

        if not isinstance(kwargs["samples_in"], np.ndarray):
            raise IncorrectTypeInStringSocketException

        kwargs["ctype"] = getattr(cv2, MAP_NUMPY_CTYPES_OPENCV_CTYPES[kwargs["samples_in"].dtype.name])

        covar_out, mean_out = self.process_cv(fn=cv2.calcCovarMatrix, kwargs=kwargs)
        self.refresh_output_socket("covar_out", covar_out, is_uuid_type=True)
        self.refresh_output_socket("mean_out", mean_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")
