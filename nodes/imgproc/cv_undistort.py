import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLundistortNode(OCVLNodeBase):

    n_doc = "Transforms an image to compensate for lens distortion."
    n_development_status = "BETA"
    n_requirements = {"__and__": ["src_in", "cameraMatrix_in", "distCoeffs_in", "newCameraMatrix_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input (distorted) image.")
    cameraMatrix_in: bpy.props.StringProperty(name="cameraMatrix_in", default=str(uuid.uuid4()), description="Input camera matrix")
    distCoeffs_in: bpy.props.StringProperty(name="distCoeffs_in", default=str(uuid.uuid4()), description="Input vector of distortion coefficients (k_1, k_2, p_1, p_2[, k_3[, k_4, k_5, k_6]]) of 4, 5, or 8 elements.")
    newCameraMatrix_in: bpy.props.StringProperty(name="newCameraMatrix_in", default=str(uuid.uuid4()), description="Camera matrix of the distorted image. By default, it is the same as cameraMatrix but you may additionally scale and shift the result by using a different matrix.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output (corrected) image.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLObjectSocket", "cameraMatrix_in")
        self.inputs.new("OCVLObjectSocket", "distCoeffs_in")
        self.inputs.new("OCVLObjectSocket", "newCameraMatrix_in")

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'cameraMatrix_in': self.get_from_props("cameraMatrix_in"),
            'distCoeffs_in': self.get_from_props("distCoeffs_in"),
            'newCameraMatrix_in': self.get_from_props("newCameraMatrix_in"),
            }

        dst_out = self.process_cv(fn=cv2.undistort, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
