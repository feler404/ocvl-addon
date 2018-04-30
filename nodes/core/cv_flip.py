import cv2
import uuid
from bpy.props import EnumProperty, StringProperty
from gettext import gettext as _

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


FLIP_CODE_ITEMS = (
    ("0", "Vertical", "Vertical", "", 0),
    ("1", "Horizontal", "Horizontal", "", 1),
    ("-1", "Simultaneous", "Simultaneous    ", "", 2),
)


class OCVLflipNode(OCVLNode):

    _doc = _("Flips a 2D array around vertical, horizontal, or both axes.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()), description="Input array.")
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()), description="Output array of the same size and type as src.")

    def get_anchor(self):
        return self.get("anchor", (-1, -1))

    flipCode_in = EnumProperty(items=FLIP_CODE_ITEMS, default='0', update=updateNode,
        description="Flag to specify how to flip the array.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
            'flipCode_in': int(self.get_from_props("flipCode_in")),
            }

        image_out = self.process_cv(fn=cv2.flip, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'flipCode_in', expand=True)


def register():
    cv_register_class(OCVLflipNode)


def unregister():
    cv_unregister_class(OCVLflipNode)
