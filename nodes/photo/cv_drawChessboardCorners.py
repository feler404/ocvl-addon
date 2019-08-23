import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLdrawChessboardCornersNode(OCVLNodeBase):

    n_doc = "Renders the detected chessboard corners."
    n_requirements = {"__and__": ["images_in",]}

    images_in: bpy.props.StringProperty(name="images_in", default=str(uuid.uuid4()), description="Destination image. It must be an 8-bit color image.")
    patternSize_in: bpy.props.StringProperty(name="patternSize_in", default=str(uuid.uuid4()), description="Number of inner corners per a chessboard row and column (patternSize = cv::Size(points_per_row,points_per_column)).")
    corners_in: bpy.props.StringProperty(name="corners_in", default=str(uuid.uuid4()), description="Array of detected corners, the output of findChessboardCorners.")
    patternWasFound: bpy.props.BoolProperty(name="patternWasFound ", default=str(uuid.uuid4()), description="Parameter indicating whether the complete board was found or not. The return value of findChessboardCorners() should be passed here.")

    image_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "images_in")
        self.inputs.new("OCVLVectorSocket", "patternSize_in")
        self.inputs.new("OCVLObjectSocket", "corners_in")

        self.outputs.new("OCVLImageSocket", "image_out")

    def wrapped_process(self):
        kwargs = {
            'images_in': [self.get_from_props("images_in")],
            'patternSize_in': self.get_from_props("patternSize_in"),
            'corners_in': self.get_from_props("corners_in"),
            'patternWasFound': self.get_from_props("patternWasFound"),
        }

        image_out = self.process_cv(fn=cv2.drawChessboardCorners, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "patternWasFound")
