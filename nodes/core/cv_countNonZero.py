import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, FloatProperty, IntProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLcountNonZeroNode(OCVLNode):

    _doc = _("")
    _note = _("")
    _see_also = _("")

    src_in = StringProperty(name="src", default=str(uuid.uuid4()), description="first input array or a scalar.")

    retval_out = IntProperty(name="retval", default=0,
        description="")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src")

        self.outputs.new("StringsSocket", "retval")

    def wrapped_process(self):
        self.check_input_requirements(["src"])

        kwargs = {
            'src': self.get_from_props("src"),
            }

        retval = self.process_cv(fn=cv2.countNonZero, kwargs=kwargs)
        self.refresh_output_socket("retval", retval, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLcountNonZeroNode)


def unregister():
    cv_unregister_class(OCVLcountNonZeroNode)
