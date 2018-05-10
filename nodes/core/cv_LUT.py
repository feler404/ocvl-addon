import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode


class OCVLLUTNode(OCVLNode):

    _doc = _("Performs a look-up table transform of an array.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input array of 8-bit elements."))
    lut_in = StringProperty(name="lut_in", default=str(uuid.uuid4()),
        description=_("Look-up table of 256 elements; in case of multi-channel input array, the table should either have a single channel (in this case the same table is used for all channels) or the same number of channels as in the input array."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output array of the same size and number of channels as src, and the same depth as lut."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "lut_in")

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in", "lut_in"])
        kwargs = {
            'src': self.get_from_props("image_in"),
            'lut_in': self.get_from_props("lut_in"),
        }

        image_out = self.process_cv(fn=cv2.LUT, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)


def register():
    cv_register_class(OCVLLUTNode)


def unregister():
    cv_unregister_class(OCVLLUTNode)
