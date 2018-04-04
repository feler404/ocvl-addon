import cv2
import uuid
import numpy as np
from bpy.props import StringProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode


class OCVLgetAffineTransformNode(OCVLNode):
    pts1_in = StringProperty(name="pts1_in", default=str(uuid.uuid4()))
    pts2_in = StringProperty(name="pts2_in", default=str(uuid.uuid4()))

    matrix_out = StringProperty(name="matrix_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "pts1_in")
        self.inputs.new("StringsSocket", "pts2_in")

        self.outputs.new("StringsSocket", "matrix_out")

    def wrapped_process(self):
        self.check_input_requirements(["pts1_in", "pts2_in"])

        pts1 = self.get_from_props("pts1_in")
        pts2 = self.get_from_props("pts2_in")
        pts1 = np.float32(pts1)
        pts2 = np.float32(pts2)
        kwargs = {
            'src': pts1,
            'dst': pts2,
        }

        matrix_out = self.process_cv(fn=cv2.getAffineTransform, kwargs=kwargs)
        self.refresh_output_socket("matrix_out", matrix_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLgetAffineTransformNode)


def unregister():
    cv_unregister_class(OCVLgetAffineTransformNode)

