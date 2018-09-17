import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLfitEllipseNode(OCVLNode):

    _doc = _("Fits an ellipse around a set of 2D points.")

    points_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Input vector of 2D points, stored in std::vector\<\> or Mat"))

    ellipse_out = StringProperty(default=str(uuid.uuid4()),
        description=_("Output ellipse."))

    loc_from_findContours = BoolProperty(default=True, update=updateNode,
        description=_("If linked with findContour node switch to True"))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "points_in")

        self.outputs.new("StringsSocket", "ellipse")

    def wrapped_process(self):
        self.check_input_requirements(["points_in"])

        kwargs = {
            'points': self.get_from_props("points_in")[0] if self.loc_from_findContours else self.get_from_props("points_in"),
            }

        ellipse = self.process_cv(fn=cv2.fitEllipse, kwargs=kwargs)
        self.refresh_output_socket("ellipse", ellipse)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'loc_from_findContours')


def register():
    cv_register_class(OCVLfitEllipseNode)


def unregister():
    cv_unregister_class(OCVLfitEllipseNode)
