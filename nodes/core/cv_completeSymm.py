import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, FloatProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLcompleteSymmNode(OCVLNode):

    _doc = _("")
    _note = _("")
    _see_also = _("")

    mtx_in = StringProperty(name="mtx_in", default=str(uuid.uuid4()),
        description="Input-output floating-point square matrix.")

    lowerToUpper_in = BoolProperty(name="lowerToUpper_in", default=False, update=updateNode,
        description="")
    mtx_out = StringProperty(name="mtx_out", default=str(uuid.uuid4()),
        description="")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "mtx_in")
        self.inputs.new("StringsSocket", "lowerToUpper_in").prop_name = "lowerToUpper_in"

        self.outputs.new("StringsSocket", "mtx_out")

    def wrapped_process(self):
        self.check_input_requirements(["mtx_in"])

        kwargs = {
            'mtx_in': self.get_from_props("mtx_in"),
            'lowerToUpper_in': self.get_from_props("lowerToUpper_in"),
            }

        mtx_out = self.process_cv(fn=cv2.completeSymm, kwargs=kwargs)
        self.refresh_output_socket("mtx_out", mtx_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLcompleteSymmNode)


def unregister():
    cv_unregister_class(OCVLcompleteSymmNode)
