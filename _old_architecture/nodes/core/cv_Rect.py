from bpy.props import IntProperty
from gettext import gettext as _
from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLRectNode(OCVLNode):

    _doc = _("Rect.")

    x_in = IntProperty(default=10, min=0, max=2048, update=updateNode,
        description=_("X input."))
    y_in = IntProperty(default=10, min=0, max=2048, update=updateNode,
        description=_("Y input."))
    width_in = IntProperty(default=10, min=0, max=2048, update=updateNode,
        description=_("Width input."))
    height_in = IntProperty(default=10, min=0, max=2048, update=updateNode,
        description=_("Height input."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "x_in").prop_name = "x_in"
        self.inputs.new("StringsSocket", "y_in").prop_name = "y_in"
        self.inputs.new("StringsSocket", "width_in").prop_name = "width_in"
        self.inputs.new("StringsSocket", "height_in").prop_name = "height_in"
        self.outputs.new("StringsSocket", "rect_out")

    def wrapped_process(self):
        x_in = self.get_from_props("x_in")
        y_in = self.get_from_props("y_in")
        width_in = self.get_from_props("width_in")
        height_in = self.get_from_props("height_in")

        rect_out = x_in, y_in, width_in, height_in
        self.refresh_output_socket("rect_out", rect_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLRectNode)


def unregister():
    cv_unregister_class(OCVLRectNode)
