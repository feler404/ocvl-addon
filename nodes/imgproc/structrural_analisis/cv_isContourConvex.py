import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLisContourConvexNode(OCVLNodeBase):

    n_doc = "Tests a contour convexity."
    n_requirements = {"__and__": ["contour_in"]}

    contour_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="Input vector of 2D points, stored in std::vector\<\> or Mat")
    loc_from_findContours: bpy.props.BoolProperty(default=True, update=update_node, description="If linked with findContour node switch to True")

    retval_out: bpy.props.BoolProperty(default=False, description="True if contour is convex")

    def init(self, context):
        self.inputs.new("ContourSocket", "contour_in")
        self.outputs.new("StringsSocket", "retval_out").prop_name = "retval_out"

    def wrapped_process(self):
        kwargs = {
            'contour_in': self.get_from_props("contour_in")[0] if self.loc_from_findContours else self.get_from_props("contour_in"),
            }

        retval_out = self.process_cv(fn=cv2.isContourConvex, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out)

    def draw_buttons(self, context, layout):
        layout.label(text='Contour is convex: {}'.format(self.retval_out))
        self.add_button(layout, 'loc_from_findContours')
