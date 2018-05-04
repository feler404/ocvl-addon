import cv2
import uuid
import numpy as np
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, COEFFICIENTS_TYPE_ITEMS, updateNode


class OCVLGetDerivKernelsNode(OCVLNode):

    _doc = _("Returns filter coefficients for computing spatial image derivatives.")

    kx_out = StringProperty(name="kx_out", default=str(uuid.uuid4()),
        description=_("Output matrix of row filter coefficients. It has the type ktype ."))
    ky_out = StringProperty(name="ky_out", default=str(uuid.uuid4()),
        description=_("Output matrix of column filter coefficients. It has the type ktype ."))
    kernel_out = StringProperty(name="kernel_out", default=str(uuid.uuid4()),
        description=_("Output kernel."))

    dx_in = IntProperty(default=3, min=1, max=10, update=updateNode,
        description=_("Derivative order in respect of x."))
    dy_in = IntProperty(default=3, min=1, max=10, update=updateNode,
        description=_("Derivative order in respect of y."))
    ksize_in = IntProperty(default=1, update=updateNode, min=1, max=30,
        description=_("Aperture size. It can be CV_SCHARR, 1, 3, 5, or 7."))
    normalize_in = BoolProperty(default=False, update=updateNode,
        description=_("Flag indicating whether to normalize (scale down) the filter coefficients or not."))
    ktype_in = EnumProperty(items=COEFFICIENTS_TYPE_ITEMS, default='CV_32F', update=updateNode,
        description=_("Type of filter coefficients. It can be CV_32f or CV_64F."))

    def sv_init(self, context):
        self.inputs.new('StringsSocket', "dx_in").prop_name = 'dx_in'
        self.inputs.new('StringsSocket', "dy_in").prop_name = 'dy_in'
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'

        self.outputs.new("StringsSocket", "kernel_out")
        self.outputs.new("StringsSocket", "kx_out")
        self.outputs.new("StringsSocket", "ky_out")

    def wrapped_process(self):

        kwargs = {
            'dx_in': self.get_from_props("dx_in"),
            'dy_in': self.get_from_props("dy_in"),
            'ksize_in': self.get_from_props("ksize_in"),
            'normalize_in': self.get_from_props("normalize_in"),
            'ktype_in': self.get_from_props("ktype_in"),
            }

        kx_out, ky_out = self.process_cv(fn=cv2.getDerivKernels, kwargs=kwargs)
        kernel_out = np.outer(kx_out, ky_out)
        self.refresh_output_socket("kx_out", kx_out, is_uuid_type=True)
        self.refresh_output_socket("ky_out", ky_out, is_uuid_type=True)
        self.refresh_output_socket("kernel_out", kernel_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'normalize_in')
        self.add_button(layout, 'ktype_in')


def register():
    cv_register_class(OCVLGetDerivKernelsNode)


def unregister():
    cv_unregister_class(OCVLGetDerivKernelsNode)
