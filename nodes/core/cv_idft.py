import cv2
import uuid
from bpy.props import StringProperty, IntProperty, BoolVectorProperty
from gettext import gettext as _

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, DEVELOP_STATE_BETA


class OCVLidftNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA
    bl_flags_list = 'DFT_INVERSE, DFT_SCALE, DFT_ROWS, DFT_COMPLEX_OUTPUT, DFT_REAL_OUTPUT'

    _doc = _("Calculates the inverse Discrete Fourier Transform of a 1D or 2D array.")

    src_in = StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input floating-point real or complex array.")
    flags_in = BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")),
        update=updateNode, subtype="NONE", description=bl_flags_list)
    nonzeroRows_in = IntProperty(default=0, min=0, update=updateNode, description="Number of dst rows to process.")

    dst_out = StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array whose size and type depend on the flags.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src_in")
        self.inputs.new("StringsSocket", "nonzeroRows_in").prop_name = "nonzeroRows_in"

        self.outputs.new("StringsSocket", "dst_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in"])

        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'nonzeroRows_in': self.get_from_props("nonzeroRows_in"),
            'flags_in': self.get_from_props("flags_in"),
            }

        dst_out = self.process_cv(fn=cv2.idft, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")


def register():
    cv_register_class(OCVLidftNode)


def unregister():
    cv_unregister_class(OCVLidftNode)
