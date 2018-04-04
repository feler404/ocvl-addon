import cv2
import uuid
from bpy.props import StringProperty, BoolProperty, FloatProperty

from ...extend.utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLarcLengthNode(OCVLNode):

    curve_in = StringProperty(default=str(uuid.uuid4()),
        description="Input vector of 2D points, stored in std::vector or Mat.")
    closed_in = BoolProperty(default=False, update=updateNode,
        description="Flag indicating whether the curve is closed or not.")
    loc_from_findContours = BoolProperty(default=True, update=updateNode,
        description="If linked with findContour node switch to True")

    length_out = FloatProperty(default=0.0,
        description="Length of contour.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "curve_in")

        self.outputs.new("StringsSocket", "length_out").prop_name = "length_out"

    def wrapped_process(self):
        self.check_input_requirements(["curve_in"])

        kwargs = {
            'curve': self.get_from_props("curve_in")[0] if self.loc_from_findContours else self.get_from_props("curve_in"),
            'closed': self.get_from_props("closed_in"),
            }

        length_out = self.process_cv(fn=cv2.arcLength, kwargs=kwargs)
        self.length_out = length_out
        self.refresh_output_socket("length_out", length_out)

    def draw_buttons(self, context, layout):
        layout.label('Length: {}'.format(self.length_out))
        self.add_button(layout, 'closed_in')
        self.add_button(layout, 'loc_from_findContours')


def register():
    cv_register_class(OCVLarcLengthNode)


def unregister():
    cv_unregister_class(OCVLarcLengthNode)
