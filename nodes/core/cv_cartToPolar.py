import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, FloatProperty, BoolProperty, BoolVectorProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLcartToPolarNode(OCVLNode):

    _doc = _("")
    _note = _("")
    _see_also = _("")


    x_in = StringProperty(name="x_in", default=str(uuid.uuid4()),
        description="")
    y_in = StringProperty(name="y_in", default=str(uuid.uuid4()),
        description="")

    angleInDegrees_in = BoolProperty(default=False, update=updateNode,
        description="")

    magnitude_out = StringProperty(name="magnitude_out", default=str(uuid.uuid4()),
        description="")
    angle_out = StringProperty(name="angle_out", default=str(uuid.uuid4()),
        description="")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "x_in")
        self.inputs.new("StringsSocket", "y_in")

        self.outputs.new("StringsSocket", "magnitude_out")
        self.outputs.new("StringsSocket", "angle_out")

    def wrapped_process(self):
        self.check_input_requirements(["x_in", "y_in"])

        kwargs = {
            'x_in': self.get_from_props("x_in"),
            'y_in': self.get_from_props("y_in"),
            'angleInDegrees_in': self.get_from_props("angleInDegrees_in"),
            }

        magnitude_out, angle_out = self.process_cv(fn=cv2.cartToPolar, kwargs=kwargs)
        self.refresh_output_socket("magnitude_out", magnitude_out, is_uuid_type=True)
        self.refresh_output_socket("angle_out", angle_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "angleInDegrees_in")


def register():
    cv_register_class(OCVLcartToPolarNode)


def unregister():
    cv_unregister_class(OCVLcartToPolarNode)
