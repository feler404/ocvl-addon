import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, FloatProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLabsdiffNode(OCVLNode):

    _doc = _("Calculates the per-element absolute difference between two arrays or between an array and a scalar.")
    _note = _(" Saturation is not applied when the arrays have the depth CV_32S. You may even get a negative value in the case of overflow.")
    _see_also = _("abs")

    src1_in = StringProperty(name="src1", default=str(uuid.uuid4()), description="first input array or a scalar.")
    src2_in = StringProperty(name="src2", default=str(uuid.uuid4()), description="second input array or a scalar.")

    dst_out = StringProperty(name="dst", default=str(uuid.uuid4()),
        description="output array that has the same size and type as input arrays.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src1")
        self.inputs.new("StringsSocket", "src2")

        self.outputs.new("StringsSocket", "dst")

    def wrapped_process(self):
        self.check_input_requirements(["src1", "src2"])

        kwargs = {
            'src1': self.get_from_props("src1"),
            'src2': self.get_from_props("src2"),
            }

        dst = self.process_cv(fn=cv2.absdiff, kwargs=kwargs)
        self.refresh_output_socket("dst", dst, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLabsdiffNode)


def unregister():
    cv_unregister_class(OCVLabsdiffNode)
