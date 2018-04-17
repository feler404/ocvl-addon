import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, COLOR_DEPTH_ITEMS, BORDER_TYPE_ITEMS


class OCVLScharrNode(OCVLNode):

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))


    dx_in = IntProperty(default=1, min=0, max=1, update=updateNode,
        description="Order of the derivative x.")
    dy_in = IntProperty(default=0, min=0, max=1, update=updateNode,
        description="Order of the derivative y.")
    ddepth_in = EnumProperty(items=COLOR_DEPTH_ITEMS, default='CV_8U', update=updateNode,
        description="Output image depth, see @ref filter_depths 'combinations'.")
    scale_in = FloatProperty(default=1.0, min=1, max=8, update=updateNode,
        description="Optional scale factor for the computed Laplacian values.")
    delta_in = FloatProperty(default=0.0, min=0, max=255, update=updateNode,
        description="Optional delta value that is added to the results prior to storing them in dst.")
    borderType_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description="Pixel extrapolation method, see cv::BorderTypes")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "dx_in").prop_name = 'dx_in'
        self.inputs.new('StringsSocket', "dy_in").prop_name = 'dy_in'
        self.inputs.new('StringsSocket', "scale_in").prop_name = 'scale_in'
        self.inputs.new('StringsSocket', "delta_in").prop_name = 'delta_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
            'ddepth_in': self.get_from_props("ddepth_in"),
            'dx_in': self.get_from_props("dx_in"),
            'dy_in': self.get_from_props("dy_in"),
            'scale_in': self.get_from_props("scale_in"),
            'delta_in': self.get_from_props("delta_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        image_out = self.process_cv(fn=cv2.Scharr, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')
        self.add_button(layout, 'ddepth_in')


def register():
    cv_register_class(OCVLScharrNode)


def unregister():
    cv_unregister_class(OCVLScharrNode)
