import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLminEnclosingTriangleNode(OCVLNodeBase):

    n_doc = "The function finds a triangle of minimum area enclosing the given set of 2D points and returns its area. The output for a given 2D point set is shown in the image below. 2D points are depicted in red and the enclosing triangle in yellow."
    n_development_status = "ALPHA"
    n_requirements = {"__and__": ["points_in"]}

    points_in: bpy.props.StringProperty(name="points_in", default=str(uuid.uuid4()), description="Input vector of 2D points with depth CV_32S or CV_32F")

    retval_out: bpy.props.StringProperty(name="retval_out", default=str(uuid.uuid4()), description="Output vector of three 2D points defining the vertices of the triangle. ")
    triangle_out: bpy.props.StringProperty(name="triangle_out", default=str(uuid.uuid4()), description="Output triangle.")

    def init(self, context):
        self.inputs.new("VectorSocket", "points_in")

        self.outputs.new("StringsSocket", "retval_out")
        self.outputs.new("StringsSocket", "triangle_out")

    def wrapped_process(self):
        kwargs = {
            'points_in': self.get_from_props("points_in"),
            }

        retval_out = self.process_cv(fn=cv2.minEnclosingTriangle, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)
        triangle_out = self.process_cv(fn=cv2.minEnclosingTriangle, kwargs=kwargs)
        self.refresh_output_socket("triangle_out", triangle_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'points_in')
