import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLmagnitudeNode(OCVLNodeBase):

    n_doc = "Calculates the magnitude of 2D vectors."
    n_requirements = {"__and__": ["x_in", "y_in"]}
    n_quick_link_requirements = {
        "x_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
        "y_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
    }

    x_in: bpy.props.StringProperty(name="x_in", default=str(uuid.uuid4()), description="Floating-point array of x-coordinates of the vectors.")
    y_in: bpy.props.StringProperty(name="y_in", default=str(uuid.uuid4()), description="Floating-point array of y-coordinates of the vectors; it must have the same size as x.")

    magnitude_out: bpy.props.StringProperty(name="magnitude_out", default=str(uuid.uuid4()),
        description="Output array of the same size and type as x.")

    def init(self, context):
        self.width = 150
        self.inputs.new("OCVLImageSocket", "x_in")
        self.inputs.new("OCVLImageSocket", "y_in")
        self.outputs.new("OCVLImageSocket", "magnitude_out")

    def wrapped_process(self):

        kwargs = {
            'x_in': self.get_from_props("x_in"),
            'y_in': self.get_from_props("y_in"),
        }

        magnitude_out = self.process_cv(fn=cv2.magnitude, kwargs=kwargs)
        self.refresh_output_socket("magnitude_out", magnitude_out, is_uuid_type=True)
