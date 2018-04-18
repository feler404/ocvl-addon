import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLconvexHullNode(OCVLNode):

    _doc=_("Finds the convex hull of a point set.")

    hull_out = StringProperty(default=str(uuid.uuid4()),
        description=_("Output convex hull. It is either an integer vector of indices or vector of points."))
    points_in = StringProperty(name="points_in", default=str(uuid.uuid4()),
        description=_("Input 2D point set, stored in std::vector or Mat."))
    clockwise_in = BoolProperty(default=False, update=updateNode,
        description=_("Orientation flag. If it is true, the output convex hull is oriented clockwise."))
    returnPoints_in = BoolProperty(default=False, update=updateNode,
        description=_("Operation flag. In case of a matrix, when the flag is true, the function returns convex hull points."))
    loc_from_findContours = BoolProperty(default=True, update=updateNode,
        description=_("If linked with findContour node switch to True"))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "points_in")

        self.outputs.new("StringsSocket", "hull_out")

    def wrapped_process(self):

        kwargs = {
            'points': self.get_from_props("points_in")[0] if self.loc_from_findContours else self.get_from_props("points_in"),
            'clockwise': self.get_from_props("clockwise_in"),
            'returnPoints': self.get_from_props("returnPoints_in"),
            }

        hull_out = self.process_cv(fn=cv2.convexHull, kwargs=kwargs)
        self.refresh_output_socket("hull_out", hull_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'clockwise_in')
        self.add_button(layout, 'returnPoints_in')
        self.add_button(layout, 'loc_from_findContours')


def register():
    cv_register_class(OCVLconvexHullNode)


def unregister():
    cv_unregister_class(OCVLconvexHullNode)
