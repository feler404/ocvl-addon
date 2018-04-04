import cv2
import uuid
from bpy.props import StringProperty, BoolProperty, BoolVectorProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, DEVELOP_STATE_BETA


class OCVLmulSpectrumsNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA
    bl_flags_list = 'DFT_ROWS'

    a_in = StringProperty(name="a_in", default=str(uuid.uuid4()))
    b_in = StringProperty(name="b_in", default=str(uuid.uuid4()))
    flags_in = BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")),
        update=updateNode, subtype="NONE", description=bl_flags_list)
    conjB_in = BoolProperty(name="conjB_in", default=False)

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "a_in")
        self.inputs.new("StringsSocket", "b_in")

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["a_in", "b_in"])

        kwargs = {
            'a_in': self.get_from_props("a_in"),
            'b_in': self.get_from_props("b_in"),
            'flags_in': self.get_from_props("flags_in"),
            'conjB_in': self.get_from_props("conjB_in"),
            }

        image_out = self.process_cv(fn=cv2.mulSpectrums, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")


def register():
    cv_register_class(OCVLmulSpectrumsNode)


def unregister():
    cv_unregister_class(OCVLmulSpectrumsNode)
