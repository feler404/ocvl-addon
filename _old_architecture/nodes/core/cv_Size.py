from bpy.props import IntProperty
from gettext import gettext as _
from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLSizeNode(OCVLNode):

    _doc = _("Size node.")

    width_in = IntProperty(default=10, min=0, max=2048, update=updateNode,
        description=_("Width input."))
    height_in = IntProperty(default=10, min=0, max=2048, update=updateNode,
        description=_("Height input."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "width_in").prop_name = "width_in"
        self.inputs.new("StringsSocket", "height_in").prop_name = "height_in"
        self.outputs.new("StringsSocket", "size_out")

    def wrapped_process(self):
        width_in = self.get_from_props("width_in")
        height_in = self.get_from_props("height_in")

        size_out = width_in, height_in
        self.refresh_output_socket("size_out", size_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLSizeNode)


def unregister():
    cv_unregister_class(OCVLSizeNode)
