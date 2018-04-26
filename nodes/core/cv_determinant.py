import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLdeterminantNode(OCVLNode):

    _doc = _("")
    _note = _("")
    _see_also = _("")

    mtx_in = StringProperty(name="mtx_in", default=str(uuid.uuid4()),
        description="Input matrix that must have CV_32FC1 or CV_64FC1 type and square size.")

    retval_out = FloatProperty(name="retval_out",
        description="")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "mtx_in")

        self.outputs.new("StringsSocket", "retval_out")

    def wrapped_process(self):
        self.check_input_requirements(["mtx_in"])

        kwargs = {
            'mtx_in': self.get_from_props("mtx_in"),
            }

        retval_out = self.process_cv(fn=cv2.determinant, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLdeterminantNode)


def unregister():
    cv_unregister_class(OCVLdeterminantNode)
