import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLminAreaRectNode(OCVLNodeBase):

    n_doc = "Finds a rotated rectangle of the minimum area enclosing the input 2D point set."
    n_requirements = {"__and__": ["points_in"]}

    points_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="Input vector of 2D points, stored in std::vector\<\> or Mat")
    loc_from_findContours: bpy.props.BoolProperty(default=True, update=update_node, description="If linked with findContour node switch to True")

    retval_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="")

    def init(self, context):
        self.inputs.new("OCVLContourSocket", "points_in")
        self.outputs.new("OCVLObjectSocket", "retval_in")

    def wrapped_process(self):
        kwargs = {
            'points_in': self.get_from_props("points_in")[0] if self.loc_from_findContours else self.get_from_props("points_in"),
            }

        retval_in = tuple(self.process_cv(fn=cv2.minAreaRect, kwargs=kwargs))
        self.refresh_output_socket("retval_in", retval_in, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'loc_from_findContours')
