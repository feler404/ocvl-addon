import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLmaxNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Calculates per-element maximum of two arrays or an array and a scalar.")

    n_id = StringProperty(default='')
    n_meta = StringProperty(default='')
    src1_in = StringProperty(name="src1_in", default=str(uuid.uuid4()),
        description=_("First input array."))
    src2_in = StringProperty(name="src2_in", default=str(uuid.uuid4()),
        description=_("Second input array of the same size and type as src1."))

    array_out = StringProperty(name="array_out", default=str(uuid.uuid4()),
        description=_("Output array of the same size and type as src1."))

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

        array_out = self.process_cv(fn=cv2.max, kwargs=kwargs)
        self.refresh_output_socket("array_out", array_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLmaxNode)


def unregister():
    cv_unregister_class(OCVLmaxNode)
