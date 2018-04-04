import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatProperty

from ...extend.utils import cv_register_class, cv_unregister_class, BORDER_TYPE_ITEMS, OCVLNode, updateNode, DEVELOP_STATE_BETA


class OCVLcornerHarrisNode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    blockSize_in = IntProperty(default=2, min=1, max=30, update=updateNode,
        description='Neighborhood size (see the details on cornerEigenValsAndVecs ).')
    ksize_in = IntProperty(default=3, min=1, max=30, update=updateNode,
        description="Aperture parameter for the Sobel operator.")
    k_in = FloatProperty(default=0.04, min=0.01, max=1, update=updateNode,
        description="Harris detector free parameter. See the formula below.")
    borderType_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description="Pixel extrapolation method. See cv::BorderTypes.")

    def sv_init(self, context):
        self.width = 150
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "blockSize_in").prop_name = 'blockSize_in'
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('StringsSocket', "k_in").prop_name = 'k_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
            'blockSize_in': self.get_from_props("blockSize_in"),
            'ksize_in': self.get_from_props("ksize_in"),
            'k_in': self.get_from_props("k_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        image_out = self.process_cv(fn=cv2.cornerHarris, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')


def register():
    cv_register_class(OCVLcornerHarrisNode)


def unregister():
    cv_unregister_class(OCVLcornerHarrisNode)
