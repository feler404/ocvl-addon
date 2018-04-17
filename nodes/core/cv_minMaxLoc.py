import cv2
import uuid
from bpy.props import StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA


class OCVLminMaxLocNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA

    src_in = StringProperty(name="src_in", default=str(uuid.uuid4()))
    mask_in = StringProperty(name="mask_in", default=str(uuid.uuid4()))

    minVal_out = StringProperty(name="minVal_out", default=str(uuid.uuid4()))
    maxVal_out = StringProperty(name="maxVal_out", default=str(uuid.uuid4()))
    minLoc_out = StringProperty(name="minLoc_out", default=str(uuid.uuid4()))
    maxLoc_out = StringProperty(name="maxLoc_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "src_in")
        self.inputs.new("StringsSocket", "mask_in")

        self.outputs.new("StringsSocket", "minVal_out")
        self.outputs.new("StringsSocket", "maxVal_out")
        self.outputs.new("StringsSocket", "minLoc_out")
        self.outputs.new("StringsSocket", "maxLoc_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in"])

        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'mask_in': self.get_from_props("mask_in"),
            }
        if isinstance(kwargs['mask_in'], str):
            kwargs.pop('mask_in')

        minVal_out, maxVal_out, minLoc_out, maxLoc_out = self.process_cv(fn=cv2.minMaxLoc, kwargs=kwargs)
        self.refresh_output_socket("minVal_out", minVal_out, is_uuid_type=True)
        self.refresh_output_socket("maxVal_out", maxVal_out, is_uuid_type=True)
        self.refresh_output_socket("minLoc_out", minLoc_out, is_uuid_type=True)
        self.refresh_output_socket("maxLoc_out", maxLoc_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLminMaxLocNode)


def unregister():
    cv_unregister_class(OCVLminMaxLocNode)
