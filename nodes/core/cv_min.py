import cv2
import uuid
from bpy.props import StringProperty

from ...utils import cv_register_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLminNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA

    src1_in = StringProperty(name="src1_in", default=str(uuid.uuid4()))
    src2_in = StringProperty(name="src2_in", default=str(uuid.uuid4()))
    array_out = StringProperty(name="array_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src1_in")
        self.inputs.new("StringsSocket", "src2_in")
        self.outputs.new("StringsSocket", "array_out")

    def wrapped_process(self):
        self.check_input_requirements(["src1_in", "src2_in"])

        kwargs = {
            'src1_in': self.get_from_props("src1_in"),
            'src2_in': self.get_from_props("src2_in"),
            }

        array_out = self.process_cv(fn=cv2.min, kwargs=kwargs)
        self.refresh_output_socket("array_out", array_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLminNode)


def unregister():
    cv_register_class(OCVLminNode)
