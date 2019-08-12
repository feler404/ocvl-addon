import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLboxPointsNode(OCVLNodeBase):

    n_doc = "Finds the four vertices of a rotated rect. Useful to draw the rotated rectangle."
    n_requirements = {"__and__": ["box_in"]}
    n_quick_link_requirements = {"box_in": {"loc_input_mode": "MANUAL", "value_type_in": "float32", "loc_manual_input": "((1.0, 0.0), (1.4, 1.4), -45.0)"}}

    box_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="Points and angle in one list.")

    def init(self, context):
        self.inputs.new("OCVLVectorSocket", "box_in")
        self.outputs.new("OCVLObjectSocket", "points_out")

    def wrapped_process(self):
        kwargs = {
            'box_in': tuple(self.get_from_props("box_in")),
            }

        points_out = self.process_cv(fn=cv2.boxPoints, kwargs=kwargs)
        self.refresh_output_socket("points_out", points_out)
