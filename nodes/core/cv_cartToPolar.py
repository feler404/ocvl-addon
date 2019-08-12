import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLcartToPolarNode(OCVLNodeBase):

    n_doc = "Calculates the magnitude and angle of 2D vectors."
    n_requirements = {"__and__": ["x_in", "y_in"]}
    n_quick_link_requirements = {
        "x_in": {"width_in": 30, "height_in": 30, "code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
        "y_in": {"width_in": 30, "height_in": 30, "code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
    }

    x_in: bpy.props.StringProperty(name="x_in", default=str(uuid.uuid4()), description="Array of x-coordinates; this must be a single-precision or double-precision floating-point array.")
    y_in: bpy.props.StringProperty(name="y_in", default=str(uuid.uuid4()), description="Array of y-coordinates, that must have the same size and same type as x.")

    angleInDegrees_in: bpy.props.BoolProperty(default=False, update=update_node, description="A flag, indicating whether the angles are measured in radians (which is by default), or in degrees.")

    magnitude_out: bpy.props.StringProperty(name="magnitude_out", default=str(uuid.uuid4()), description="Output array of magnitudes of the same size and type as x.")
    angle_out: bpy.props.StringProperty(name="angle_out", default=str(uuid.uuid4()), description="Output array of angles that has the same size and type as x; the angles are measured in radians (from 0 to 2*Pi) or in degrees (0 to 360 degrees).")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "x_in")
        self.inputs.new("OCVLImageSocket", "y_in")

        self.outputs.new("OCVLObjectSocket", "magnitude_out")
        self.outputs.new("OCVLObjectSocket", "angle_out")

    def wrapped_process(self):
        kwargs = {
            'x_in': self.get_from_props("x_in"),
            'y_in': self.get_from_props("y_in"),
            'angleInDegrees_in': self.get_from_props("angleInDegrees_in"),
            }

        magnitude_out, angle_out = self.process_cv(fn=cv2.cartToPolar, kwargs=kwargs)
        self.refresh_output_socket("magnitude_out", magnitude_out, is_uuid_type=True)
        self.refresh_output_socket("angle_out", angle_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "angleInDegrees_in")
