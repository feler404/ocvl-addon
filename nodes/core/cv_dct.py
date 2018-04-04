import cv2
import uuid
from bpy.props import StringProperty, BoolVectorProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, DEVELOP_STATE_BETA


class OCVLdctNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA
    bl_flags_list = 'DCT_INVERSE, DCT_ROWS'

    src_in = StringProperty(name="src_in", default=str(uuid.uuid4()))
    flags_in = BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")),
        update=updateNode, subtype="NONE", description=bl_flags_list)

    dst_out = StringProperty(name="dst_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src_in")

        self.outputs.new("StringsSocket", "dst_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in"])
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'flags_in': self.get_from_props("flags_in"),
            }

        dst_out = self.process_cv(fn=cv2.dct, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")


def register():
    cv_register_class(OCVLdctNode)


def unregister():
    cv_unregister_class(OCVLdctNode)
