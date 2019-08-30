import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLfillConvexPolyNode(OCVLNodeBase):

    n_doc = "Fills a convex polygon."
    n_requirements = {"__and__": ["img_in", "pts_in", "color_in"]}

    img_in: bpy.props.StringProperty(name="img_in", default=str(uuid.uuid4()),  description="Input Image.")
    points_in: bpy.props.StringProperty(name="points_in", default=str(uuid.uuid4()),  description="Polygon vertices")
    color_in: bpy.props.StringProperty(name="color_in", default=str(uuid.uuid4()), update=update_node, description="Polygon color.")

    img_out: bpy.props.StringProperty(name="img_out", default=str(uuid.uuid4()), description="Output Image.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "img_in")
        self.inputs.new("OCVLVectorSocket", "points_in")
        self.inputs.new("OCVLVectorSocket", "color_in")

        self.outputs.new("OCVLImageSocket", "img_out")

    def wrapped_process(self):
        kwargs = {
            'img_in': self.get_from_props("img_in"),
            'points_in': self.get_from_props("points_in"),
            'color_in': self.get_from_props("color_in"),
            }

        img_out = self.process_cv(fn=cv2.fillConvexPoly, kwargs=kwargs)
        self.refresh_output_socket("img_out", img_out, is_uuid_type=True)
