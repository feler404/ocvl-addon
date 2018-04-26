import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLmixChannelsNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Copies specified channels from input arrays to the specified channels of output arrays.")

    src_in = StringProperty(name="src_in", default=str(uuid.uuid4()),
        description=_("Input array or vector of matrices; all of the matrices must have the same size and the same depth."))
    fromTo_in = StringProperty(name="fromTo_in", default=str(uuid.uuid4()),
        description=_("Array of index pairs specifying which channels are copied and where."))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output array or vector of matrices."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src_in")
        self.inputs.new("StringsSocket", "fromTo_in")

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in", "fromTo_in"])

        src_in = self.get_from_props("src_in")
        dst_in = src_in.copy()

        kwargs = {
            'src_in': src_in,
            'dst_in': dst_in,
            'fromTo_in': self.get_from_props("fromTo_in"),
            }

        image_out = self.process_cv(fn=cv2.mixChannels, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLmixChannelsNode)


def unregister():
    cv_unregister_class(OCVLmixChannelsNode)
