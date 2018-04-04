import cv2
import uuid
from bpy.props import StringProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode


class OCVLinvertAffineTransformNode(OCVLNode):

    matrix_invert_in = StringProperty(name="matrix_invert_in", default=str(uuid.uuid4()))
    matrix_invert_out = StringProperty(name="matrix_invert_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "matrix_invert_in")
        self.outputs.new("StringsSocket", "matrix_invert_out")

    def wrapped_process(self):
        kwargs = {
            'M_in': self.get_from_props("matrix_invert_in"),
            }

        matrix_invert_out = self.process_cv(fn=cv2.invertAffineTransform, kwargs=kwargs)
        self.refresh_output_socket("matrix_invert_out", matrix_invert_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLinvertAffineTransformNode)


def unregister():
    cv_unregister_class(OCVLinvertAffineTransformNode)
