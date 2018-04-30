import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLeigenNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Calculates eigenvalues and eigenvectors of a symmetric matrix.")

    src_in = StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input matrix that must have CV_32FC1 or CV_64FC1 type, square size and be symmetrical.")

    retval_out = StringProperty(name="retval_out", default=str(uuid.uuid4()))
    eigenvalues_out = StringProperty(name="eigenvalues_out", default=str(uuid.uuid4()), description="Output vector of eigenvalues of the same type as src; the eigenvalues are stored in the descending order.")
    eigenvectors_out = StringProperty(name="eigenvectors_out", default=str(uuid.uuid4()), description="Output matrix of eigenvectors; it has the same size and type as src.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src_in")

        self.outputs.new("StringsSocket", "retval_out")
        self.outputs.new("StringsSocket", "eigenvalues_out")
        self.outputs.new("StringsSocket", "eigenvectors_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in"])
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            }

        retval_out, eigenvalues_out, eigenvectors_out = self.process_cv(fn=cv2.eigen, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)
        self.refresh_output_socket("eigenvalues_out", eigenvalues_out, is_uuid_type=True)
        self.refresh_output_socket("eigenvectors_out", eigenvectors_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLeigenNode)


def unregister():
    cv_unregister_class(OCVLeigenNode)
