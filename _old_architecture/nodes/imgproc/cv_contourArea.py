import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLcontourAreaNode(OCVLNode):

    _doc = _("Calculates a contour area.")

    contour_in = StringProperty(name="contour_in", default=str(uuid.uuid4()),
        description=_("Input vector of 2D points (contour vertices), stored in std::vector or Mat."))
    area_out = FloatProperty(default=0.0,
        description=_("Area of contour."))
    oriented_out = BoolProperty(default=False, update=updateNode,
        description=_("Oriented area flag. If it is true, the function returns a signed area value, depending on the contour orientation (clockwise or counter-clockwise)."))
    loc_from_findContours = BoolProperty(default=True, update=updateNode,
        description=_("If linked with findContour node switch to True"))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "contour_in")
        self.outputs.new("StringsSocket", "area_out").prop_name = "area_out"

    def wrapped_process(self):

        kwargs = {
            'contour': self.get_from_props("contour_in")[0] if self.loc_from_findContours else self.get_from_props("contour_in"),
            'oriented': self.get_from_props("oriented_out"),
            }

        area_out = self.process_cv(fn=cv2.contourArea, kwargs=kwargs)
        self.area_out = area_out
        self.refresh_output_socket("area_out", area_out)

    def draw_buttons(self, context, layout):
        layout.label('Area: {}'.format(self.area_out))
        self.add_bount(layout, 'oriented_out')
        self.add_bount(layout, 'loc_from_findContours')


def register():
    cv_register_class(OCVLcontourAreaNode)


def unregister():
    cv_unregister_class(OCVLcontourAreaNode)
