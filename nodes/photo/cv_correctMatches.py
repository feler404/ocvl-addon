import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLcorrectMatchesNode(OCVLNodeBase):

    n_doc = "Refines coordinates of corresponding points"
    n_requirements = {"__and__": [""]}
    n_quick_link_requirements = {
        "channels_in": {"loc_input_mode": "MANUAL", "loc_manual_input": "(0, 1, 2)"},
        "histSize_in": {"loc_input_mode": "MANUAL", "loc_manual_input": "(8, 8, 8)"},
        "ranges_in": {"loc_input_mode": "MANUAL", "loc_manual_input": "(0, 180, 0, 256, 0, 256)"},
    }

    F_in: bpy.props.StringProperty(name="F_in", default=str(uuid.uuid4()), description="3x3 fundamental matrix.")
    points1_in: bpy.props.StringProperty(name="points1_in ", default=str(uuid.uuid4()), description="1xN array containing the first set of points.")
    points2_in: bpy.props.StringProperty(name="points2_in ", default=str(uuid.uuid4()), description="1xN array containing the second set of points.")

    newPoints1_out: bpy.props.StringProperty(name="newPoints1_out", default=str(uuid.uuid4()), description="The optimized points1.")
    newPoints2_out: bpy.props.StringProperty(name="newPoints2_out", default=str(uuid.uuid4()), description="The optimized points2.")

    def init(self, context):
        self.inputs.new("OCVLObjectSocket", "F_in")
        self.inputs.new("OCVLVectorSocket", "points1_in")
        self.inputs.new("OCVLVectorSocket", "points2_in")

        self.outputs.new("OCVLObjectSocket", "newPoints1_out")
        self.outputs.new("OCVLObjectSocket", "newPoints2_out")

    def wrapped_process(self):
        kwargs = {
            'F_in': [self.get_from_props("F_in")],
            'points1_in': self.get_from_props("points1_in"),
            'points2_in': self.get_from_props("points2_in"),
        }

        newPoints1_out, newPoints2_out = self.process_cv(fn=cv2.correctMatches, kwargs=kwargs)
        self.refresh_output_socket("newPoints1_out", newPoints1_out, is_uuid_type=True)
        self.refresh_output_socket("newPoints2_out", newPoints2_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass
