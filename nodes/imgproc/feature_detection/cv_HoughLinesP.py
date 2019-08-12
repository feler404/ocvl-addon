import uuid

import bpy
import cv2
import numpy as np
from ocvl.core.node_base import OCVLNodeBase, update_node

OUTPUT_MODE_ITEMS = (
    ("LINES", "LINES", "LINES", "", 0),
    ("IMAGE", "IMAGE", "IMAGE", "", 1),
)


PROPS_MAPS = {
    OUTPUT_MODE_ITEMS[0][0]: ("lines_out",),
    OUTPUT_MODE_ITEMS[1][0]: ("lines_out", "image_out"),
}


class OCVLHoughLinesPNode(OCVLNodeBase):

    n_doc = "Finds line segments in a binary image using the probabilistic Hough transform."
    n_requirements = {"__and__": ["image_in"]}
    n_quick_link_requirements = {"image_in": {"code_in": "COLOR_BGR2GRAY"}}

    def update_layout(self, context):
        self.update_sockets(context)
        update_node(self, context)

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()), description="Input image.")
    rho_in: bpy.props.FloatProperty(default=3, min=1, max=10, update=update_node, description="Distance resolution of the accumulator in pixels.")
    theta_in: bpy.props.FloatProperty(default=0.0574, min=0.0001, max=3.1415, update=update_node, description="Angle resolution of the accumulator in radians.")
    threshold_in: bpy.props.IntProperty(default=200, min=0, max=255, update=update_node, description="Accumulator threshold parameter.")
    minLineLength_in: bpy.props.FloatProperty(default=0, min=0, update=update_node, description="Minimum line length. Line segments shorter than that are rejected.")
    maxLineGap_in: bpy.props.FloatProperty(default=0, min=0, update=update_node, description="Maximum allowed gap between points on the same line to link them.")

    loc_output_mode: bpy.props.EnumProperty(items=OUTPUT_MODE_ITEMS, default="LINES", update=update_layout, description="Output mode.")
    lines_out: bpy.props.StringProperty(name="lines_out", default=str(uuid.uuid4()), description="Output vector of lines.")
    image_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "image_in")
        self.inputs.new('OCVLObjectSocket', "rho_in").prop_name = 'rho_in'
        self.inputs.new('OCVLObjectSocket', "theta_in").prop_name = 'theta_in'
        self.inputs.new('OCVLObjectSocket', "threshold_in").prop_name = 'threshold_in'
        self.inputs.new('OCVLObjectSocket', "minLineLength_in").prop_name = 'minLineLength_in'
        self.inputs.new('OCVLObjectSocket', "maxLineGap_in").prop_name = 'maxLineGap_in'

        self.outputs.new("OCVLObjectSocket", "lines_out")

    def wrapped_process(self):
        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'rho_in': int(self.get_from_props("rho_in")),
            'theta_in': self.get_from_props("theta_in"),
            'threshold_in': int(self.get_from_props("threshold_in")),
            'minLineLength_in': int(self.get_from_props("minLineLength_in")),
            'maxLineGap_in': int(self.get_from_props("maxLineGap_in")),
            }

        lines_out = self.process_cv(fn=cv2.HoughLinesP, kwargs=kwargs)
        self.refresh_output_socket("lines_out", lines_out, is_uuid_type=True)
        if self.loc_output_mode == "IMAGE":
            image = np.copy(self.get_from_props("image_in"))
            image_out = self._draw_hough_lines(lines_out, image)
            self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def update_sockets(self, context):
        self.update_sockets_for_node_mode(PROPS_MAPS, self.loc_output_mode)
        self.process()

    def _draw_hough_lines(self, lines, image):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 1)
        return image

    def draw_buttons(self, context, layout):
        self.add_button(layout, "loc_output_mode")
