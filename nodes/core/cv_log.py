import cv2
import uuid
from bpy.props import StringProperty
from gettext import gettext as _

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLlogNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Calculates the natural logarithm of every array element.")

    array_in = StringProperty(name="array_in", default=str(uuid.uuid4()), description="Input array.")
    array_out = StringProperty(name="array_out", default=str(uuid.uuid4()), description="Iutput array of the same size and type as input array .")


    def sv_init(self, context):
        self.width = 150
        self.inputs.new("StringsSocket", "array_in")
        self.outputs.new("StringsSocket", "array_out")

    def wrapped_process(self):
        self.check_input_requirements(["array_in"])

        kwargs = {
            'src': self.get_from_props("array_in"),
            }

        array_out = self.process_cv(fn=cv2.log, kwargs=kwargs)
        self.refresh_output_socket("array_out", array_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLlogNode)


def unregister():
    cv_unregister_class(OCVLlogNode)
