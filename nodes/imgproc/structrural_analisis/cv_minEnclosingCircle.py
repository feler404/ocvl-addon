import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLminEnclosingCircleNode(OCVLNodeBase):

    n_doc = "Finds a circle of the minimum area enclosing a 2D point set."
    n_requirements = {"__and__": ["points_in"]}

    points_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="Input vector of 2D points, stored in std::vector\<\> or Mat")
    loc_from_findContours: bpy.props.BoolProperty(default=True, update=update_node, description="If linked with findContour node switch to True")

    def init(self, context):
        self.inputs.new("OCVLContourSocket", "points_in")

        self.outputs.new("OCVLObjectSocket", "center_out")
        self.outputs.new("OCVLObjectSocket", "radius_out")

    def wrapped_process(self):
        kwargs = {
            'points_in': self.get_from_props("points_in")[0] if self.loc_from_findContours else self.get_from_props("points_in"),
            }

        (x, y), radius_out = self.process_cv(fn=cv2.minEnclosingCircle, kwargs=kwargs)
        self.refresh_output_socket("center_out", (int(x), int(y)))
        self.refresh_output_socket("radius_out", int(radius_out))

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'loc_from_findContours')
