import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLboundingRectNode(OCVLNode):

    _doc = _("Calculates the up-right bounding rectangle of a point set.")

    points_in = StringProperty(default=str(uuid.uuid4()), update=updateNode,
        description=_("Input 2D point set, stored in std::vector or Mat."))

    pt1_out = IntVectorProperty(default=(0, 0), size=2, description=_("Pt1 output."))
    pt2_out = IntVectorProperty(default=(0, 0), size=2, description=_("Pt2 output."))

    loc_from_findContours = BoolProperty(default=True, update=updateNode,
        description=_("If linked with findContour node switch to True"))

    def sv_init(self, context):
        self.inputs.new('StringsSocket', "points_in")

        self.outputs.new("StringsSocket", "pt1_out")
        self.outputs.new("StringsSocket", "pt2_out")

    def wrapped_process(self):
        self.check_input_requirements(["points_in"])

        kwargs = {
            'points': self.get_from_props("points_in")[0] if self.loc_from_findContours else self.get_from_props("points_in"),
            }

        x, y, w, h = self.process_cv(fn=cv2.boundingRect, kwargs=kwargs)
        pt1_out, pt2_out = (x, y), (x + w, y + h)
        self.refresh_output_socket("pt1_out", pt1_out)
        self.refresh_output_socket("pt2_out", pt2_out)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'loc_from_findContours')


def register():
    cv_register_class(OCVLboundingRectNode)


def unregister():
    cv_unregister_class(OCVLboundingRectNode)
