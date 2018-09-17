import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, BoolProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode, DISTANCE_TYPE_ITEMS


class OCVLfitLineNode(OCVLNode):

    _doc = _("Fits a line to a 2D or 3D point set.")

    points_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Input vector of 2D points, stored in std::vector\<\> or Mat"))
    distType_in = EnumProperty(items=DISTANCE_TYPE_ITEMS, default="DIST_L1", update=updateNode,
        description=_("Distance used by the M-estimator, see cv::DistanceTypes."))
    param_in = FloatProperty(default=0, min=0, max=1,
        description=_("Numerical parameter ( C ) for some types of distances. If it is 0, an optimal value is chosen."))
    reps_in = FloatProperty(default=0, min=0, max=1,
        description=_("Sufficient accuracy for the radius (distance between the coordinate origin and the line)."))
    aeps_in = FloatProperty(default=0.01, min=0, max=1,
        description=_("Sufficient accuracy for the angle. 0.01 would be a good default value for reps and aeps."))
    loc_from_findContours = BoolProperty(default=True, update=updateNode,
        description=_("If linked with findContour node switch to True"))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "points_in")
        self.inputs.new("StringsSocket", "param_in").prop_name = "param_in"
        self.inputs.new("StringsSocket", "reps_in").prop_name = "reps_in"
        self.inputs.new("StringsSocket", "aeps_in").prop_name = "aeps_in"

        self.outputs.new("StringsSocket", "pt1_out")
        self.outputs.new("StringsSocket", "pt2_out")

    def wrapped_process(self):
        self.check_input_requirements(["points_in"])

        kwargs = {
            'points': self.get_from_props("points_in")[0] if self.loc_from_findContours else self.get_from_props("points_in"),
            'distType': self.get_from_props("distType_in"),
            'param': self.get_from_props("param_in"),
            'reps': self.get_from_props("reps_in"),
            'aeps': self.get_from_props("aeps_in"),
            }

        [vx, vy, x, y] = self.process_cv(fn=cv2.fitLine, kwargs=kwargs)
        self.refresh_output_socket("pt1_out", (vx, vy))
        self.refresh_output_socket("pt2_out", (x, y))

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'loc_from_findContours')


def register():
    cv_register_class(OCVLfitLineNode)


def unregister():
    cv_unregister_class(OCVLfitLineNode)
