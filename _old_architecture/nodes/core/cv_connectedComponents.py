import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, COLOR_DEPTH_WITH_NONE_ITEMS

CONNECTIVITY_ITEMS = (
    ("8", "8", "8", "", 0),
    ("4", "4", "4", "", 1),
)

LTYPE_ITEMS = (
    ("CV_16U", "CV_16U", "CV_16U", "", 0),
    ("CV_32S", "CV_32S", "CV_32S", "", 1),
)


class OCVLconnectedComponentsNode(OCVLNode):

    _doc = _("Connected components.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("The 8-bit single-channel image to be labeled."))
    connectivity_in = EnumProperty(items=CONNECTIVITY_ITEMS, default="8", update=updateNode,
        description=_("8 or 4 for 8-way or 4-way connectivity respectively."))
    ltype_in = EnumProperty(items=LTYPE_ITEMS, default="CV_16U", update=updateNode,
        description=_("Output image label type. Currently CV_32S and CV_16U are supported."))

    labels_out = StringProperty(name="labels_out", default=str(uuid.uuid4()),
        description=_("Labels output."))
    retval_out = StringProperty(name="retval_out", default=str(uuid.uuid4()),
        description=_("Return value."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")

        self.outputs.new("StringsSocket", "labels_out")
        self.outputs.new("StringsSocket", "retval_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'connectivity_in': int(self.get_from_props("connectivity_in")),
            'ltype_in': self.get_from_props("ltype_in"),
            }

        retval_out, labels_out = self.process_cv(fn=cv2.connectedComponents, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)
        self.refresh_output_socket("labels_out", labels_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "connectivity_in", expand=True)
        self.add_button(layout, "ltype_in", expand=True)


def register():
    cv_register_class(OCVLconnectedComponentsNode)


def unregister():
    cv_unregister_class(OCVLconnectedComponentsNode)
