import cv2
import uuid
from bpy.props import StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode


class OCVLequalizeHistNode(OCVLNode):

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
        }

        image_out = self.process_cv(fn=cv2.equalizeHist, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)


def register():
    cv_register_class(OCVLequalizeHistNode)


def unregister():
    cv_unregister_class(OCVLequalizeHistNode)
