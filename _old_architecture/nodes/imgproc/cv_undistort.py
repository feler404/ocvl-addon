import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLundistortNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Transforms an image to compensate for lens distortion.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input (distorted) image."))
    cameraMatrix_in = StringProperty(name="cameraMatrix_in", default=str(uuid.uuid4()),
        description=_("Input camera matrix"))
    distCoeffs_in = StringProperty(name="distCoeffs_in", default=str(uuid.uuid4()),
        description=_("Input vector of distortion coefficients (k_1, k_2, p_1, p_2[, k_3[, k_4, k_5, k_6]]) of 4, 5, or 8 elements."))
    newCameraMatrix_in = StringProperty(name="newCameraMatrix_in", default=str(uuid.uuid4()),
        description=_("Camera matrix of the distorted image. By default, it is the same as cameraMatrix but you may additionally scale and shift the result by using a different matrix."))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output (corrected) image."))

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
