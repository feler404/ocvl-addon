import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, FloatProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, COLOR_DEPTH_WITH_NONE_ITEMS, \
    NORMALIZATION_TYPE_ITEMS, DEVELOP_STATE_ALPHA


class OCVLnormalizeNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_ALPHA

    _doc = _("Normalizes the norm or value range of an array.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input array."))
    alpha_in = FloatProperty(default=0, min=0.0, max=1000, update=updateNode,
        description=_("Norm value to normalize to or the lower range boundary in case of the range normalization."))
    beta_in = FloatProperty(default=255, min=0.0, max=1000, update=updateNode,
        description=_("Upper range boundary in case of the range normalization; it is not used for the norm normalization."))
    norm_type_in = EnumProperty(items=NORMALIZATION_TYPE_ITEMS,default="NORM_L2", update=updateNode,
        description=_("Normalization type (see cv::NormTypes)."))
    dtype_in = EnumProperty(items=COLOR_DEPTH_WITH_NONE_ITEMS, default='None', update=updateNode,
        description=_("Channels as src and the depth =CV_MAT_DEPTH(dtype)."))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output array."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "alpha_in").prop_name = 'alpha_in'
        self.inputs.new('StringsSocket', "beta_in").prop_name = 'beta_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        image_in = self.get_from_props("image_in")
        dst = image_in.copy()
        dtype = self.get_from_props("dtype_in")
        dtype = -1 if dtype is None else dtype
        kwargs = {
            'src': self.get_from_props("image_in"),
            'dst': dst,
            'alpha_in': self.get_from_props("alpha_in"),
            'beta_in': self.get_from_props("beta_in"),
            'norm_type_in': self.get_from_props("norm_type_in"),
            'dtype': dtype
            }

        image_out = self.process_cv(fn=cv2.normalize, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "norm_type_in")
        self.add_button(layout, "dtype_in", expand=True)


def register():
    cv_register_class(OCVLnormalizeNode)


def unregister():
    cv_unregister_class(OCVLnormalizeNode)
