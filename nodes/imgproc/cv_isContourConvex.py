import cv2
import uuid
from bpy.props import StringProperty, BoolProperty

from ...extend.utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLisContourConvexNode(OCVLNode):

    is_convex_out = BoolProperty(default=False,
        description="True if contour is convex")
    contour_in = StringProperty(default=str(uuid.uuid4()),
        description="Input vector of 2D points, stored in std::vector\<\> or Mat")
    loc_from_findContours = BoolProperty(default=True, update=updateNode,
        description="If linked with findContour node switch to True")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "contour_in")

        self.outputs.new("StringsSocket", "is_convex_out").prop_name = "is_convex_out"

    def wrapped_process(self):

        kwargs = {
            'contour_in': self.get_from_props("contour_in")[0] if self.loc_from_findContours else self.get_from_props("contour_in"),
            }

        is_convex_out = self.process_cv(fn=cv2.isContourConvex, kwargs=kwargs)
        self.is_convex_out = is_convex_out
        self.refresh_output_socket("is_convex_out", is_convex_out)

    def draw_buttons(self, context, layout):
        layout.label('Contour is convex: {}'.format(self.is_convex_out))
        self.add_button(layout, 'loc_from_findContours')


def register():
    cv_register_class(OCVLisContourConvexNode)


def unregister():
    cv_unregister_class(OCVLisContourConvexNode)
