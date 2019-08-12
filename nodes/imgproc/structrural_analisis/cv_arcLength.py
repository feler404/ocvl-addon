import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLarcLengthNode(OCVLNodeBase):

    n_doc = "Calculates a contour perimeter or a curve length."
    n_requirements = {"__and__": ["curve_in"]}

    curve_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="Input vector of 2D points, stored in std::vector or Mat.")
    closed_in: bpy.props.BoolProperty(default=False, update=update_node, description="Flag indicating whether the curve is closed or not.")
    loc_from_findContours: bpy.props.BoolProperty(default=True, update=update_node, description="If linked with findContour node switch to True.")

    retval_out: bpy.props.FloatProperty(default=0.0, description="Length of contour.")

    def init(self, context):
        self.inputs.new("OCVLContourSocket", "curve_in")
        self.outputs.new("OCVLObjectSocket", "retval_out").prop_name = "retval_out"

    def wrapped_process(self):
        kwargs = {
            'curve_in': self.get_from_props("curve_in")[0] if self.loc_from_findContours else self.get_from_props("curve_in"),
            'closed_in': self.get_from_props("closed_in"),
            }

        retval_out = self.process_cv(fn=cv2.arcLength, kwargs=kwargs)
        self.retval_out = retval_out
        self.refresh_output_socket("retval_out", retval_out)

    def draw_buttons(self, context, layout):
        layout.label(text='Length: {}'.format(self.retval_out))
        self.add_button(layout, 'closed_in')
        self.add_button(layout, 'loc_from_findContours')
