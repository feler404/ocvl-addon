import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, COEFFICIENTS_TYPE_ITEMS


class OCVLgetGaussianKernelNode(OCVLNode):

    _doc = _("Returns Gaussian filter coefficients.")

    kernel_out = StringProperty(name="kernel_out", default=str(uuid.uuid4()),
        description=_("Output kernel."))

    ksize_in = IntProperty(default=5, update=updateNode, min=1, max=30,
        description=_("Aperture size. It should be odd."))
    sigma_in = FloatProperty(default=0.35, min=0, max=1, update=updateNode,
        description=_("Gaussian standard deviation."))
    # normalize_in = BoolProperty(default=False, update=updateNode,
    #     description='Flag indicating whether to normalize (scale down) the filter coefficients or not.')
    ktype_in = EnumProperty(items=COEFFICIENTS_TYPE_ITEMS, default='CV_32F', update=updateNode,
        description=_("Type of filter coefficients. It can be CV_32f or CV_64F."))

    def sv_init(self, context):
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('StringsSocket', "sigma_in").prop_name = 'sigma_in'

        self.outputs.new("StringsSocket", "kernel_out")

    def wrapped_process(self):

        kwargs = {
            'ksize_in': self.get_from_props("ksize_in"),
            'sigma_in': self.get_from_props("sigma_in"),
            'ktype_in': self.get_from_props("ktype_in"),
            }

        kernel_out = self.process_cv(fn=cv2.getGaussianKernel, kwargs=kwargs)
        self.refresh_output_socket("kernel_out", kernel_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'ktype_in')


def register():
    cv_register_class(OCVLgetGaussianKernelNode)


def unregister():
    cv_unregister_class(OCVLgetGaussianKernelNode)
