import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, IntVectorProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, BORDER_TYPE_ITEMS, OCVLNode, updateNode


class OCVLGaussianBlurNode(OCVLNode):
    bl_icon = 'FILTER'

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    ksize_in = IntVectorProperty(default=(1, 1), min=1, max=30, size=2, update=updateNode,
        description='Gaussian kernel size.')
    sigmaX_in = FloatProperty(default=0, min=0, max=255, update=updateNode,
        description='Gaussian kernel standard deviation in X direction.')
    sigmaY_in = FloatProperty(default=0, min=0, max=255, update=updateNode,
        description='Gaussian kernel standard deviation in Y direction.')
    borderType_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description="Pixel extrapolation method, see cv::BorderTypes")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('StringsSocket', "sigmaX_in").prop_name = 'sigmaX_in'
        self.inputs.new('StringsSocket', "sigmaY_in").prop_name = 'sigmaY_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
            'ksize_in': self.get_from_props("ksize_in"),
            'sigmaX_in': self.get_from_props("sigmaX_in"),
            'sigmaY_in': self.get_from_props("sigmaY_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        image_out = self.process_cv(fn=cv2.GaussianBlur, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "borderType_in")


def register():
    cv_register_class(OCVLGaussianBlurNode)


def unregister():
    cv_unregister_class(OCVLGaussianBlurNode)
