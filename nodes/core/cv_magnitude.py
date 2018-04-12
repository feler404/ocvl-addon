import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLmagnitudeNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Calculates the magnitude of 2D vectors.")

    x_in = StringProperty(name="x_in", default=str(uuid.uuid4()),
        description=_("floating-point array of x-coordinates of the vectors"))
    y_in = StringProperty(name="y_in", default=str(uuid.uuid4()),
        description=_("floating-point array of y-coordinates of the vectors; it must have the same size as x"))
    array_out = StringProperty(name="array_out", default=str(uuid.uuid4()),
        description=_("output array of the same size and type as x"))

    def sv_init(self, context):
        self.width = 150
        self.inputs.new("StringsSocket", "x_in")
        self.inputs.new("StringsSocket", "y_in")
        self.outputs.new("StringsSocket", "array_out")

    def wrapped_process(self):
        self.check_input_requirements(["x_in", "y_in"])

        kwargs = {
            'x_in': self.get_from_props("x_in"),
            'y_in': self.get_from_props("y_in"),
            }

        array_out = self.process_cv(fn=cv2.magnitude, kwargs=kwargs)
        self.refresh_output_socket("array_out", array_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLmagnitudeNode)


def unregister():
    cv_unregister_class(OCVLmagnitudeNode)
