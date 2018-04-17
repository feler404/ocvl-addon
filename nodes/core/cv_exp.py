import cv2
import uuid
from bpy.props import StringProperty
from gettext import gettext as _

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLexpNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Calculates the exponent of every array element.")

    src_in = StringProperty(name="src_in", default=str(uuid.uuid4()), description=_("Input array."))
    dst_out = StringProperty(name="dst_out", default=str(uuid.uuid4()), description=_("Output array of the same size and type as input array."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src_in")

        self.outputs.new("StringsSocket", "dst_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in"])

        kwargs = {
            'src_in': self.get_from_props("src_in"),
            }

        dst_out = self.process_cv(fn=cv2.exp, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLexpNode)


def unregister():
    cv_unregister_class(OCVLexpNode)
