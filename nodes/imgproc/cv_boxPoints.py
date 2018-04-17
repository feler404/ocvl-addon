import cv2
import uuid
from bpy.props import StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode


class OCVLboxPointsNode(OCVLNode):

    rect_in = StringProperty(default=str(uuid.uuid4()),
        description="Points and angle in one list")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "rect_in")

        self.outputs.new("StringsSocket", "points_out")

    def wrapped_process(self):
        self.check_input_requirements(["rect_in"])

        kwargs = {
            'box': tuple(self.get_from_props("rect_in")),
            }

        points_out = self.process_cv(fn=cv2.boxPoints, kwargs=kwargs)
        self.refresh_output_socket("points_out", points_out)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLboxPointsNode)


def unregister():
    cv_unregister_class(OCVLboxPointsNode)
