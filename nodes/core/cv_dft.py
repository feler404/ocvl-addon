import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, IntProperty, BoolVectorProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, DEVELOP_STATE_BETA


class OCVLdftNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA
    bl_flags_list = 'DFT_INVERSE, DFT_SCALE, DFT_ROWS, DFT_COMPLEX_OUTPUT, DFT_REAL_OUTPUT'

    _doc = _("Performs a forward or inverse Discrete Fourier transform of a 1D or 2D floating-point array.")
    _note = _("")

    src_in = StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array that could be real or complex.")
    flags_in = BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")),
        update=updateNode, subtype="NONE", description=bl_flags_list)
    nonzeroRows_in = IntProperty(default=0, min=0, update=updateNode,
        description="when the parameter is not zero, the function assumes that only the first nonzeroRows rows of the input array (DFT_INVERSE is not set) or only the first nonzeroRows of the output array (DFT_INVERSE is set) contain non-zeros.")

    array_out = StringProperty(name="array_out", default=str(uuid.uuid4()), description="Output array whose size and type depends on the flags.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src_in")
        self.inputs.new("StringsSocket", "nonzeroRows_in").prop_name = "nonzeroRows_in"

        self.outputs.new("StringsSocket", "array_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in"])

        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'nonzeroRows_in': self.get_from_props("nonzeroRows_in"),
            'flags_in': self.get_from_props("flags_in"),
            }

        array_out = self.process_cv(fn=cv2.dft, kwargs=kwargs)
        self.refresh_output_socket("array_out", array_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")


def register():
    cv_register_class(OCVLdftNode)


def unregister():
    cv_unregister_class(OCVLdftNode)
