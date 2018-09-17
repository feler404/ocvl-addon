import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, IntVectorProperty, BoolVectorProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, BORDER_MODE_ITEMS, DEVELOP_STATE_BETA


class OCVLwarpPerspectiveNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA
    bl_flags_list = 'INTER_LINEAR, WARP_FILL_OUTLIERS'

    _doc = _("Applies a perspective transformation to an image.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Image input."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Image output."))

    M_in = StringProperty(name="M_in", default=str(uuid.uuid4()),
        description=_("Transformation matrix."))

    dsize_in = IntVectorProperty(default=(100, 100), update=updateNode, min=1, max=2028, size=2,
        description=_("Size of the output image."))
    flags_in = BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")),
        update=updateNode, subtype="NONE", description=bl_flags_list)
    borderMode_in = EnumProperty(items=BORDER_MODE_ITEMS, default='BORDER_CONSTANT', update=updateNode,
        description=_("Pixel extrapolation method (BORDER_CONSTANT or BORDER_REPLICATE)."))
    borderValue_in = IntProperty(default=0, min=0, max=255, update=updateNode,
        description=_("Value used in case of a constant border; by default, it equals 0."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "M_in")
        self.inputs.new('StringsSocket', "dsize_in").prop_name = 'dsize_in'
        self.inputs.new('StringsSocket', "borderValue_in").prop_name = 'borderValue_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in", "M_in"])

        kwargs = {
            'src_in': self.get_from_props("image_in"),
            'M_in': self.get_from_props("M_in"),
            'dsize_in': self.get_from_props("dsize_in"),
            'flags_in': self.get_from_props("flags_in"),
            'borderMode_in': self.get_from_props("borderMode_in"),
            'borderValue_in': self.get_from_props("borderValue_in"),
            }

        image_out = self.process_cv(fn=cv2.warpPerspective, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")
        self.add_button(layout, "borderMode_in")


def register():
    cv_register_class(OCVLwarpPerspectiveNode)


def unregister():
    cv_unregister_class(OCVLwarpPerspectiveNode)
