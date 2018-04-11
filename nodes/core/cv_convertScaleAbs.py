import cv2
import uuid
from bpy.props import StringProperty, FloatProperty
from gettext import gettext as _
from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, DEVELOP_STATE_RC


class OCVLconvertScaleAbsNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_RC

    _doc = "Scales, calculates absolute values, and converts the result to 8-bit."
    _note = _("")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()), description="Input image.")
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()), description="Output image.")

    alpha_in = FloatProperty(default=1, min=0.0, max=100, update=updateNode,
        description="Optional scale factor.")
    beta_in = FloatProperty(default=0, min=0.0, max=100, update=updateNode,
        description="Optional delta added to the scaled values.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "alpha_in").prop_name = 'alpha_in'
        self.inputs.new('StringsSocket', "beta_in").prop_name = 'beta_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
            'alpha_in': self.get_from_props("alpha_in"),
            'beta_in': self.get_from_props("beta_in"),
            }

        image_out = self.process_cv(fn=cv2.convertScaleAbs, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLconvertScaleAbsNode)


def unregister():
    cv_unregister_class(OCVLconvertScaleAbsNode)


