import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, FONT_FACE_ITEMS, updateNode


class OCVLgetTextSizeNode(OCVLNode):
    bl_icon = 'GREASEPENCIL'

    _doc = _("Calculates the width and height of a text string.")

    baseLine_out = StringProperty(name="baseLine_out", default=str(uuid.uuid4()),
        description=_("Output parameter - y-coordinate of the baseline relative to the bottom-most text point."))
    retval_out = StringProperty(name="retval_out", default=str(uuid.uuid4()))

    text_in = StringProperty(default="OpenCV", update=updateNode,
        description=_("Text string to be drawn."))
    fontScale_in = IntProperty(default=5, min=1, max=30,update=updateNode,
        description=_("Scale factor that is multiplied by the font-specific base size."))
    fontFace_in = EnumProperty(items=FONT_FACE_ITEMS, default="FONT_HERSHEY_SIMPLEX", update=updateNode,
        description=_("Font type, see cv::HersheyFonts."))
    thickness_in = IntProperty(default=2, min=1, max=10, update=updateNode,
        description=_("Thickness of the lines used to draw a text."))

    def sv_init(self, context):
        self.inputs.new('StringsSocket', "text_in").prop_name = 'text_in'
        self.inputs.new('StringsSocket', "fontScale_in").prop_name = 'fontScale_in'
        self.inputs.new('StringsSocket', "thickness_in").prop_name = 'thickness_in'

        self.outputs.new("StringsSocket", "baseLine_out")
        self.outputs.new("StringsSocket", "retval_out")

    def wrapped_process(self):
        self.check_input_requirements([])

        kwargs = {
            'text_in': self.get_from_props("text_in"),
            'fontFace_in': self.get_from_props("fontFace_in"),
            'fontScale_in': self.get_from_props("fontScale_in"),
            'thickness_in': self.get_from_props("thickness_in"),
            }

        retval_out, baseLine_out = self.process_cv(fn=cv2.getTextSize, kwargs=kwargs)
        self.refresh_output_socket("baseLine_out", baseLine_out, is_uuid_type=True)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "fontFace")


def register():
    cv_register_class(OCVLgetTextSizeNode)


def unregister():
    cv_unregister_class(OCVLgetTextSizeNode)
