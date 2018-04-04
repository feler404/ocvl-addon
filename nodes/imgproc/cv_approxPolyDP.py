import cv2
import uuid
from bpy.props import StringProperty, BoolProperty, FloatProperty

from ...extend.utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLapproxPolyDPNode(OCVLNode):

    curve_in = StringProperty(name="curve_in", default=str(uuid.uuid4()),
        description="Input vector of a 2D point stored in std::vector or Mat")
    epsilon_in = FloatProperty(default=0.1,
        description="Parameter specifying the approximation accuracy. This is the maximum distance")
    closed_in = BoolProperty(default=False, update=updateNode,
        description="If true, the approximated curve is closed (its first and last vertices are connected). Otherwise, it is not closed.")

    approxCurve_out = StringProperty(default=str(uuid.uuid4()),
        description="Result of the approximation. The type should match the type of the input curve.")

    loc_from_findContours = BoolProperty(default=True, update=updateNode,
        description="If linked with findContour node switch to True")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "curve_in")
        self.inputs.new("StringsSocket", "epsilon_in").prop_name = "epsilon_in"

        self.outputs.new("StringsSocket", "approxCurve_out").prop_name = "approxCurve_out"

    def wrapped_process(self):
        self.check_input_requirements(["curve_in"])

        kwargs = {
            'curve': self.get_from_props("curve_in")[0] if self.loc_from_findContours else self.get_from_props("curve_in"),
            'epsilon': self.get_from_props("epsilon_in"),
            'closed': self.get_from_props("closed_in"),
            }

        approxCurve_out = self.process_cv(fn=cv2.approxPolyDP, kwargs=kwargs)
        self.refresh_output_socket("approxCurve_out", approxCurve_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'closed_in')
        self.add_button(layout, 'loc_from_findContours')


def register():
    cv_register_class(OCVLapproxPolyDPNode)


def unregister():
    cv_unregister_class(OCVLapproxPolyDPNode)
