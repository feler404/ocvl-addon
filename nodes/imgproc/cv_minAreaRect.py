import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLminAreaRectNode(OCVLNode):

    _doc = _("Finds a rotated rectangle of the minimum area enclosing the input 2D point set.")

    points_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Input vector of 2D points, stored in std::vector\<\> or Mat"))
    loc_from_findContours = BoolProperty(default=True, update=updateNode,
        description=_("If linked with findContour node switch to True"))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "points_in")

        self.outputs.new("StringsSocket", "points_out")

    def wrapped_process(self):

        kwargs = {
            'points_in': self.get_from_props("points_in")[0] if self.loc_from_findContours else self.get_from_props("points_in"),
            }

        points_out = tuple(self.process_cv(fn=cv2.minAreaRect, kwargs=kwargs))
        self.refresh_output_socket("points_out", points_out)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'loc_from_findContours')


def register():
    cv_register_class(OCVLminAreaRectNode)


def unregister():
    cv_unregister_class(OCVLminAreaRectNode)
