import cv2
import uuid
from bpy.props import StringProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLundistortNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    cameraMatrix_in = StringProperty(name="cameraMatrix_in", default=str(uuid.uuid4()))
    distCoeffs_in = StringProperty(name="distCoeffs_in", default=str(uuid.uuid4()))
    newCameraMatrix_in = StringProperty(name="newCameraMatrix_in", default=str(uuid.uuid4()))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "cameraMatrix_in")
        self.inputs.new("StringsSocket", "distCoeffs_in")
        self.inputs.new("StringsSocket", "newCameraMatrix_in")

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in", "cameraMatrix_in", "distCoeffs_in", "newCameraMatrix_in"])

        kwargs = {
            'src_in': self.get_from_props("image_in"),
            'cameraMatrix_in': self.get_from_props("cameraMatrix_in"),
            'distCoeffs_in': self.get_from_props("distCoeffs_in"),
            'newCameraMatrix_in': self.get_from_props("newCameraMatrix_in"),
            }

        image_out = self.process_cv(fn=cv2.undistort, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLundistortNode)


def unregister():
    cv_unregister_class(OCVLundistortNode)
