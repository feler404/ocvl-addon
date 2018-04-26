import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, BORDER_TYPE_ITEMS, OCVLNode, updateNode


class OCVLbilateralFilterNode(OCVLNode):
    bl_icon = 'FILTER'

    d_in = IntProperty(default=2, min=1, max=10, update=updateNode,
        description="Diameter of each pixel neighborhood that is used during filtering. If it is non-positive, it is computed from sigmaSpace.")
    sigmaColor_in = FloatProperty(default=75, min=0, max=255, update=updateNode,
        description="Filter sigma in the color space.")
    sigmaSpace_in = FloatProperty(default=75, min=0, max=255, update=updateNode,
        description="Filter sigma in the coordinate space.")
    borderType_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description="Border mode used to extrapolate pixels outside of the image, see cv::BorderTypes.")

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.width = 150
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "d_in").prop_name = 'd_in'
        self.inputs.new('StringsSocket', "sigmaColor_in").prop_name = 'sigmaColor_in'
        self.inputs.new('StringsSocket', "sigmaSpace_in").prop_name = 'sigmaSpace_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
            'd_in': self.get_from_props("d_in"),
            'sigmaColor_in': self.get_from_props("sigmaColor_in"),
            'sigmaSpace_in': self.get_from_props("sigmaSpace_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        image_out = self.process_cv(fn=cv2.bilateralFilter, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')


def register():
    cv_register_class(OCVLbilateralFilterNode)


def unregister():
    cv_unregister_class(OCVLbilateralFilterNode)
