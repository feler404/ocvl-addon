import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, BORDER_TYPE_ITEMS


class OCVLborderInterpolateNode(OCVLNode):

    _doc = _("Computes the source location of an extrapolated pixel.")
    _note = _("")
    _see_also = _("")

    p_in = IntProperty(name="p", default=5, update=updateNode,
        description=_("0-based coordinate of the extrapolated pixel along one of the axes, likely <0 or >= len ."))
    len_in = IntProperty(name="len", default=10, update=updateNode,
        description=_("Length of the array along the corresponding axis."))
    borderType_in = EnumProperty(name="borderType", items=BORDER_TYPE_ITEMS, default='BORDER_DEFAULT', update=updateNode,
        description=_("Pixel extrapolation method, see cv::BorderTypes"))

    retval_out = IntProperty(name="retval", default=0, description="")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "p").prop_name = "p_in"
        self.inputs.new("StringsSocket", "len").prop_name = "len_in"

        self.outputs.new("StringsSocket", "retval")

    def wrapped_process(self):
        self.check_input_requirements([])

        kwargs = {
            'p': self.get_from_props("p_in"),
            'len': self.get_from_props("len_in"),
            'borderType': self.get_from_props("borderType_in"),
            }

        retval = self.process_cv(fn=cv2.borderInterpolate, kwargs=kwargs)
        self.refresh_output_socket("retval", retval)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "borderType_in")


def register():
    cv_register_class(OCVLborderInterpolateNode)


def unregister():
    cv_unregister_class(OCVLborderInterpolateNode)
