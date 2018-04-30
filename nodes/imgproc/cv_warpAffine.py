import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, IntVectorProperty, BoolVectorProperty

from ...utils import cv_register_class, cv_unregister_class, BORDER_TYPE_ITEMS, OCVLNode, updateNode, DEVELOP_STATE_ALPHA


class OCVLwarpAffineNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_ALPHA
    bl_flags_list = 'INTER_LINEAR, INTER_NEAREST, WARP_INVERSE_MAP'

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    M_in = StringProperty(name="M_in", default=str(uuid.uuid4()),
        description="Transformation matrix.")

    dsize_in = IntVectorProperty(default=(100, 100), update=updateNode, min=1, max=2028, size=2,
        description='Size of the output image.')
    flags_in = BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")),
        update=updateNode, subtype="NONE", description=bl_flags_list)
    borderMode_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description="border mode used to extrapolate pixels outside of the image, see cv::BorderTypes")
    borderValue_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description="border mode used to extrapolate pixels outside of the image, see cv::BorderTypes")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "M_in")
        self.inputs.new('StringsSocket', "dsize_in").prop_name = 'dsize_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in", "M_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
            'M_in': self.get_from_props("M_in"),
            'dsize_in': self.get_from_props("dsize_in"),
            'flags_in': self.get_from_props("flags_in"),
            }

        image_out = self.process_cv(fn=cv2.warpAffine, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")


def register():
    cv_register_class(OCVLwarpAffineNode)


def unregister():
    cv_unregister_class(OCVLwarpAffineNode)
