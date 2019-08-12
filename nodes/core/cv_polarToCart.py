import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase


class OCVLpolarToCartNode(OCVLNodeBase):

    n_doc = "Calculates x and y coordinates of 2D vectors from their magnitude and angle."
    n_requirements = {"__and__": ["magnitude_in", "angle"]}
    n_quick_link_requirements = {
        "magnitude_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
        "angle": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
    }

    magnitude_in: bpy.props.StringProperty(name="magnitude_in", default=str(uuid.uuid4()), description="Input floating-point array of magnitudes of 2D vectors.")
    angle: bpy.props.StringProperty(name="angle", default=str(uuid.uuid4()), description="Input floating-point array of angles of 2D vectors.")
    angleInDegrees_in: bpy.props.BoolProperty(name="angleInDegrees_in", default=False, description="When true, the function calculates the angle in degrees, otherwise, they are measured in radians.")

    x_out: bpy.props.StringProperty(name="x_out", default=str(uuid.uuid4()), description="Output array of x-coordinates of 2D vectors; it has the same size and type as angle.")
    y_out: bpy.props.StringProperty(name="y_out", default=str(uuid.uuid4()), description="Output array of y-coordinates of 2D vectors; it has the same size and type as angle.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "magnitude_in")
        self.inputs.new("OCVLImageSocket", "angle")
        self.outputs.new("OCVLObjectSocket", "x_out")
        self.outputs.new("OCVLObjectSocket", "y_out")

    def wrapped_process(self):
        kwargs = {
            'magnitude_in': self.get_from_props("magnitude_in"),
            'angle': self.get_from_props("angle"),
            'angleInDegrees_in': self.get_from_props("angleInDegrees_in"),
            }

        x_out, y_out = self.process_cv(fn=cv2.polarToCart, kwargs=kwargs)
        self.refresh_output_socket("x_out", x_out, is_uuid_type=True)
        self.refresh_output_socket("y_out", y_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "angleInDegrees_in")