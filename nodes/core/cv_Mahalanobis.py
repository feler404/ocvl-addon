import cv2
import uuid
from bpy.props import StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLMahalanobisNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA

    v1_in = StringProperty(name="v1_in", default=str(uuid.uuid4()))
    v2_in = StringProperty(name="v2_in", default=str(uuid.uuid4()))
    icovar_in = StringProperty(name="icovar_in", default=str(uuid.uuid4()))

    retval_out = StringProperty(name="retval_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "v1_in")
        self.inputs.new("StringsSocket", "v2_in")
        self.inputs.new("StringsSocket", "icovar_in")

        self.outputs.new("StringsSocket", "retval_out")

    def wrapped_process(self):
        self.check_input_requirements(["v1_in", "v2_in", "icovar_in"])

        kwargs = {
            'v1_in': self.get_from_props("v1_in"),
            'v2_in': self.get_from_props("v2_in"),
            'icovar_in': self.get_from_props("icovar_in"),
            }

        retval_out = self.process_cv(fn=cv2.Mahalanobis, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLMahalanobisNode)


def unregister():
    cv_unregister_class(OCVLMahalanobisNode)
