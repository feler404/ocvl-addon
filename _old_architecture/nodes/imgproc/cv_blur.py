import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, BORDER_TYPE_ITEMS, OCVLNode, updateNode, DEVELOP_STATE_BETA


class OCVLblurNode(OCVLNode):

    _doc = _("Blurs an image using the normalized box filter.")

    bl_icon = 'FILTER'
    bl_develop_state = DEVELOP_STATE_BETA

    def get_anchor(self):
        return self.get("anchor_in", (-1, -1))

    def set_anchor(self, value):
        anchor_x = value[0] if -1 <= value[0] < self.ksize_in[0] else self.anchor_in[0]
        anchor_y = value[1] if -1 <= value[1] < self.ksize_in[1] else self.anchor_in[1]
        self["anchor_in"] = (anchor_x, anchor_y)

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    ksize_in = IntVectorProperty(default=(1, 1), update=updateNode, min=1, max=30, size=2,
        description=_("Blurring kernel size."))
    anchor_in = IntVectorProperty(default=(-1, -1), update=updateNode, get=get_anchor, set=set_anchor, size=2,
        description=_("Bnchor point; default value Point(-1,-1) means that the anchor is at the kernel center."))
    borderType_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description=_("Border mode used to extrapolate pixels outside of the image, see cv::BorderTypes."))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))

    def sv_init(self, context):
        self.width = 150
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('StringsSocket', "anchor_in").prop_name = 'anchor_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
            'ksize_in': self.get_from_props("ksize_in"),
            'anchor_in': self.get_from_props("anchor_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        image_out = self.process_cv(fn=cv2.blur, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def generate_code(self, prop_name, exit_prop_name):
        lines = []
        if prop_name == 'image_out':
            if self.inputs["image_in"].is_linked:
                node_linked = self.inputs["image_in"].links[0].from_node
                socket_name = self.inputs["image_in"].links[0].from_socket.name
                lines.extend(node_linked.generate_code(socket_name, "src"))
            lines.append('ksize_in = {}'.format(self.get_from_props("ksize_in")))
            lines.append("{} = cv2.blur(src=src, ksize_in=ksize_in)".format(exit_prop_name))
        return lines

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')


def register():
    cv_register_class(OCVLblurNode)


def unregister():
    cv_unregister_class(OCVLblurNode)
