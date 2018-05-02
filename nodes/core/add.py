import cv2
import uuid
from bpy.props import EnumProperty, StringProperty
from gettext import gettext as _

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA, updateNode


class OCVLaddNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Calculates the per-element sum of two arrays or an array and a scalar.")

    image_1_in = StringProperty(name="image_1_in", default=str(uuid.uuid4()), description=_("First input array or a scalar."))
    image_2_in = StringProperty(name="image_2_in", default=str(uuid.uuid4()), description=_("Second input array or a scalar."))
    mask_in = StringProperty(name="mask_in", default=str(uuid.uuid4()),
        description=_("Optional operation mask, 8-bit single channel array, that specifies elements of the output array to be changed."))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_1_in")
        self.inputs.new('StringsSocket', "mask_in")
        self.inputs.new("StringsSocket", "image_2_in")

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_1_in", "image_2_in"])

        kwargs = {
            'src1': self.get_from_props("image_1_in"),
            'src2': self.get_from_props("image_2_in"),
            'mask': self.get_from_props("mask_in"),
            }

        if isinstance(kwargs['mask'], str):
            kwargs.pop('mask')

        image_out = self.process_cv(fn=cv2.add, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)


def register():
    cv_register_class(OCVLaddNode)


def unregister():
    cv_unregister_class(OCVLaddNode)
