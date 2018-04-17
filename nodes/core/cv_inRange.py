import cv2
import uuid
from bpy.props import StringProperty
from gettext import gettext as _

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLinRangeNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Checks if array elements lie between the elements of two other arrays.")

    src_in = StringProperty(name="src_in", default=str(uuid.uuid4()), description=_("First input array."))
    lowerb_in = StringProperty(name="lowerb_in", default=str(uuid.uuid4()), description=_("Inclusive lower boundary array or a scalar."))
    upperb_in = StringProperty(name="upperb_in", default=str(uuid.uuid4()), description=_("Inclusive upper boundary array or a scalar."))

    dst_out = StringProperty(name="dst_out", default=str(uuid.uuid4()), description=_("Output array of the same size as src and CV_8U type."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src_in")
        self.inputs.new("StringsSocket", "lowerb_in")
        self.inputs.new("StringsSocket", "upperb_in")

        self.outputs.new("StringsSocket", "dst_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in", "lowerb_in", "upperb_in"])
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'lowerb_in': self.get_from_props("lowerb_in"),
            'upperb_in': self.get_from_props("upperb_in"),
            }

        dst_out = self.process_cv(fn=cv2.inRange, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLinRangeNode)


def unregister():
    cv_unregister_class(OCVLinRangeNode)
