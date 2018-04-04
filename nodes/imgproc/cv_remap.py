import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, IntProperty

from ...extend.utils import cv_register_class, cv_unregister_class, BORDER_TYPE_ITEMS, OCVLNode, updateNode, \
    INTERPOLATION_ITEMS


class OCVLremapNode(OCVLNode):

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    map1_in = StringProperty(name="map1_in", default=str(uuid.uuid4()))
    map2_in = StringProperty(name="map2_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    interpolation_in = EnumProperty(items=INTERPOLATION_ITEMS, default='INTER_NEAREST', update=updateNode,
        description="Interpolation method.")
    borderMode_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description="Border mode used to extrapolate pixels outside of the image, see cv::BorderTypes.")
    borderValue_in = IntProperty(default=0, min=0, max=255, update=updateNode,
        description="Value used in case of a constant border; by default, it equals 0.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "map1_in")
        self.inputs.new("StringsSocket", "map2_in")
        self.inputs.new('StringsSocket', "borderValue_in").prop_name = 'borderValue_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in", "map1_in", "map2_in"])

        kwargs = {
            'src_in': self.get_from_props("image_in"),
            'map1_in': self.get_from_props("map1_in"),
            'map2_in': self.get_from_props("map2_in"),
            'interpolation_in': self.get_from_props("interpolation_in"),
            'borderMode_in': self.get_from_props("borderMode_in"),
            'borderValue_in': self.get_from_props("borderValue_in"),
            }

        image_out = self.process_cv(fn=cv2.remap, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'interpolation_in')
        self.add_button(layout, 'borderMode_in')


def register():
    cv_register_class(OCVLremapNode)


def unregister():
    cv_unregister_class(OCVLremapNode)
