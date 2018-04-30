import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, FloatProperty
from gettext import gettext as _

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, DEVELOP_STATE_BETA, COLOR_DEPTH_WITH_NONE_ITEMS


class OCVLdivideNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Performs per-element division of two arrays or a scalar by an array.")

    src_1_in = StringProperty(name="src_1_in", default=str(uuid.uuid4()), description="First input array.")
    src_2_in = StringProperty(name="src_2_in", default=str(uuid.uuid4()), description="Second input array of the same size and type as src1.")
    scale_in = FloatProperty(default=1, min=1, description="Scalar factor.")
    dtype_in = EnumProperty(items=COLOR_DEPTH_WITH_NONE_ITEMS, default='None', update=updateNode,
        description="Desired depth of the destination image, see @ref filter_depths 'combinations'.")

    array_out = StringProperty(name="array_out", default=str(uuid.uuid4()), description="Output array.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src_1_in")
        self.inputs.new("StringsSocket", "src_2_in")
        self.inputs.new("StringsSocket", "scale_in").prop_name = "scale_in"

        self.outputs.new("StringsSocket", "array_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_1_in", "src_2_in"])

        kwargs = {
            'src1_in': self.get_from_props("src_1_in"),
            'src2_in': self.get_from_props("src_2_in"),
            'scale_in': self.get_from_props("scale_in"),
            'dtype_in': self.get_from_props("dtype_in"),
            }

        array_out = self.process_cv(fn=cv2.divide, kwargs=kwargs)
        self.refresh_output_socket("array_out", array_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "dtype_in")


def register():
    cv_register_class(OCVLdivideNode)


def unregister():
    cv_unregister_class(OCVLdivideNode)
