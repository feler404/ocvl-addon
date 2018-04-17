import cv2
import uuid
from bpy.props import StringProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLmomentsNode(OCVLNode):

    moments_out = StringProperty(name="moments_out", default=str(uuid.uuid4()))
    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    binaryImage_in = BoolProperty(default=False, update=updateNode,
        description="If it is true, all non-zero image pixels are treated as 1's. The parameter is used for images only.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")

        self.outputs.new("StringsSocket", "moments_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'array': self.get_from_props("image_in"),
            'binaryImage': self.get_from_props("binaryImage_in"),
            }

        moments_out = self.process_cv(fn=cv2.moments, kwargs=kwargs)
        self.refresh_output_socket("moments_out", moments_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'binaryImage_in')


def register():
    cv_register_class(OCVLmomentsNode)


def unregister():
    cv_unregister_class(OCVLmomentsNode)
