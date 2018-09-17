import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, COLOR_DEPTH_WITH_NONE_ITEMS

AUTO_RESIZE_ITEMS = (
    ("OFF", "OFF", "Resize OFF", "", 0),
    ("FIRST", "FIRST", "Resize first", "", 1),
    ("SECOND", "SECOND", "Resize second", "", 2),
)


class OCVLaddWeightedNode(OCVLNode):

    _doc = _("Calculates the weighted sum of two arrays.")
    _note = _("")

    image_1_in = StringProperty(name="image_1_in", default=str(uuid.uuid4()), description=_("First input array."))
    image_2_in = StringProperty(name="image_2_in", default=str(uuid.uuid4()), description=_("Second input array."))
    alpha_in = FloatProperty(default=0.3, min=0.0, max=1.0, update=updateNode,
        description=_("Weight of the first array elements."))
    beta_in = FloatProperty(default=0.7, min=0.0, max=1.0, update=updateNode,
        description=_("Weight of the second array elements."))
    gamma_in = FloatProperty(default=0.0, min=0.0, max=1.0, update=updateNode,
        description=_("Scalar added to each sum."))
    dtype_in = EnumProperty(items=COLOR_DEPTH_WITH_NONE_ITEMS, default='None', update=updateNode,
        description=_("Desired depth of the destination image, see @ref filter_depths 'combinations'."))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()), description=_("Output image."))

    loc_auto_resize = EnumProperty(items=AUTO_RESIZE_ITEMS, default="SECOND", update=updateNode,
        description=_("Automatic adjust size image."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_1_in")
        self.inputs.new("StringsSocket", "image_2_in")
        self.inputs.new('StringsSocket', "alpha_in").prop_name = 'alpha_in'
        self.inputs.new('StringsSocket', "beta_in").prop_name = 'beta_in'
        self.inputs.new('StringsSocket', "gamma_in").prop_name = 'gamma_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_1_in", "image_2_in"])

        image_1_in = self.get_from_props("image_1_in")
        image_2_in = self.get_from_props("image_2_in")
        dtype_in = self.get_from_props("dtype_in")
        kwargs = {
            'src1': image_1_in if self.loc_auto_resize != "FIRST" else cv2.resize(image_1_in, image_2_in.shape[::-1][1:]),
            'src2': image_2_in if self.loc_auto_resize != "SECOND" else cv2.resize(image_2_in, image_1_in.shape[::-1][1:]),
            'alpha_in': self.get_from_props("alpha_in"),
            'beta_in': self.get_from_props("beta_in"),
            'gamma_in': self.get_from_props("gamma_in"),
            'dtype_in': -1 if dtype_in is None else dtype_in
            }

        image_out = self.process_cv(fn=cv2.addWeighted, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "loc_auto_resize", expand=True)
        self.add_button(layout, "dtype_in", expand=True)


def register():
    cv_register_class(OCVLaddWeightedNode)


def unregister():
    cv_unregister_class(OCVLaddWeightedNode)
