import cv2
import uuid
from bpy.props import StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_ALPHA


class OCVLundistortPointsNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_ALPHA

    src_in = StringProperty(name="src_in", default=str(uuid.uuid4()))
    cameraMatrix_in = StringProperty(name="cameraMatrix_in", default=str(uuid.uuid4()))
    distCoeffs_in = StringProperty(name="distCoeffs_in", default=str(uuid.uuid4()))
    R_in = StringProperty(name="R_in", default=str(uuid.uuid4()))
    P_in = StringProperty(name="P_in", default=str(uuid.uuid4()))

    dst_out = StringProperty(name="dst_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src_in")
        self.inputs.new("StringsSocket", "cameraMatrix_in")
        self.inputs.new("StringsSocket", "distCoeffs_in")
        self.inputs.new("StringsSocket", "R_in")
        self.inputs.new("StringsSocket", "P_in")

        self.outputs.new("StringsSocket", "dst_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in", "cameraMatrix_in", "distCoeffs_in", "R_in", "P_in"])

        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'cameraMatrix_in': self.get_from_props("cameraMatrix_in"),
            'distCoeffs_in': self.get_from_props("distCoeffs_in"),
            'R_in': self.get_from_props("R_in"),
            'P_in': self.get_from_props("P_in"),
            }

        dst_out = self.process_cv(fn=cv2.undistortPoints, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLundistortPointsNode)


def unregister():
    cv_unregister_class(OCVLundistortPointsNode)
