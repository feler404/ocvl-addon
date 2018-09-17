import cv2
import uuid
import numpy as np
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, DEVELOP_STATE_ALPHA

OUTPUT_MODE_ITEMS = (
    ("LINES", "LINES", "LINES", "", 0),
    ("IMAGE", "IMAGE", "IMAGE", "", 1),
)


PROPS_MAPS = {
    OUTPUT_MODE_ITEMS[0][0]: ("lines_out",),
    OUTPUT_MODE_ITEMS[1][0]: ("lines_out", "image_out"),
}


class OCVLHoughLinesPNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_ALPHA

    _doc = _("Finds line segments in a binary image using the probabilistic Hough transform.")

    def update_layout(self, context):
        self.update_sockets(context)
        updateNode(self, context)

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    rho_in = FloatProperty(default=3, min=1, max=10, update=updateNode,
        description=_("Distance resolution of the accumulator in pixels."))
    theta_in = FloatProperty(default=0.0574, min=0.0001, max=3.1415, update=updateNode,
        description=_("Angle resolution of the accumulator in radians."))
    threshold_in = IntProperty(default=200, min=0, max=255, update=updateNode,
        description=_("Accumulator threshold parameter."))
    minLineLength_in = FloatProperty(default=0, min=0, update=updateNode,
        description=_("Minimum line length. Line segments shorter than that are rejected."))
    maxLineGap_in = FloatProperty(default=0, min=0, update=updateNode,
        description=_("Maximum allowed gap between points on the same line to link them."))

    loc_output_mode = EnumProperty(items=OUTPUT_MODE_ITEMS, default="LINES", update=update_layout,
        description=_("Output mode."))
    lines_out = StringProperty(name="lines_out", default=str(uuid.uuid4()),
        description=_("Output vector of lines."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "rho_in").prop_name = 'rho_in'
        self.inputs.new('StringsSocket', "theta_in").prop_name = 'theta_in'
        self.inputs.new('StringsSocket', "threshold_in").prop_name = 'threshold_in'
        self.inputs.new('StringsSocket', "minLineLength_in").prop_name = 'minLineLength_in'
        self.inputs.new('StringsSocket', "maxLineGap_in").prop_name = 'maxLineGap_in'

        self.outputs.new("StringsSocket", "lines_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

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


def register():
    cv_register_class(OCVLHoughLinesPNode)


def unregister():
    cv_unregister_class(OCVLHoughLinesPNode)
