import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, FloatProperty, BoolProperty, BoolVectorProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


COMPARE_FLAG_ITEMS = (
    ("CMP_EQ", "CMP_EQ", "CMP_EQ", "", 0),
    ("CMP_GT", "CMP_GT", "CMP_GT", "", 1),
    ("CMP_GE", "CMP_GE", "CMP_GE", "", 2),
    ("CMP_LT", "CMP_LT", "CMP_LT", "", 3),
    ("CMP_LE", "CMP_LE", "CMP_LE", "", 4),
    ("CMP_NE", "CMP_NE", "CMP_NE", "", 5),
)

class OCVLcompareNode(OCVLNode):

    _doc = _("")
    _note = _("")
    _see_also = _("")

    bl_flags_list = 'CMP_EQ, CMP_GT, CMP_GE, CMP_LT, CMP_LE, CMP_NE'


    src1_in = StringProperty(name="src1_in", default=str(uuid.uuid4()),
        description="")
    src2_in = StringProperty(name="src2_in", default=str(uuid.uuid4()),
        description="")

    cmpop_in = EnumProperty(items=COMPARE_FLAG_ITEMS, default="CMP_EQ", update=updateNode,
        description="")

    dst_out = StringProperty(name="dst_out", default=str(uuid.uuid4()),
        description="")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src1_in")
        self.inputs.new("StringsSocket", "src2_in")

        self.outputs.new("StringsSocket", "dst_out")

    def wrapped_process(self):
        self.check_input_requirements(["src1_in", "src2_in"])

        kwargs = {
            'src1_in': self.get_from_props("src1_in"),
            'src2_in': self.get_from_props("src2_in"),
            'cmpop_in': self.get_from_props("cmpop_in"),
            }

        dst_out = self.process_cv(fn=cv2.compare, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "cmpop_in")


def register():
    cv_register_class(OCVLcompareNode)


def unregister():
    cv_unregister_class(OCVLcompareNode)
