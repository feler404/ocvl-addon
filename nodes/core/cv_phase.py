import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase


class OCVLphaseNode(OCVLNodeBase):

    n_doc = "Calculates the rotation angle of 2D vectors."
    n_requirements = {"__and__": ["x_in", "y_in"]}
    n_quick_link_requirements = {
        "x_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
        "y_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
    }

    x_in: bpy.props.StringProperty(name="x_in", default=str(uuid.uuid4()), description="Input floating-point array of x-coordinates of 2D vectors.")
    y_in: bpy.props.StringProperty(name="y_in", default=str(uuid.uuid4()), description="Input array of y-coordinates of 2D vectors; it must have the same size and the same type as x.")
    angleInDegrees_in: bpy.props.BoolProperty(name="angleInDegrees_in", default=False, description="When true, the function calculates the angle in degrees, otherwise, they are measured in radians.")

    angle_out: bpy.props.StringProperty(name="angle_out", default=str(uuid.uuid4()), description="Output array of vector angles; it has the same size and same type as x.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "x_in")
        self.inputs.new("OCVLImageSocket", "y_in")
        self.outputs.new("OCVLMatrixSocket", "angle_out")

    def wrapped_process(self):
        kwargs = {
            'x_in': self.get_from_props("x_in"),
            'y_in': self.get_from_props("y_in"),
            'angleInDegrees_in': self.get_from_props("angleInDegrees_in"),
            }

        angle_out = self.process_cv(fn=cv2.phase, kwargs=kwargs)
        self.refresh_output_socket("angle_out", angle_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "angleInDegrees_in")