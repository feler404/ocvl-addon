import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, BORDER_TYPE_ITEMS


class OCVLGaussianBlurNode(OCVLNodeBase):

    bl_icon = 'FILTER'

    n_doc = "Blurs an image using a Gaussian filter."
    n_requirements = {"__and__": ["src_in"]}

    def set_ksize(self, value):
        ksize_x = value[0] if value[0] % 2 != 0 else value[0] + 1
        ksize_y = value[1] if value[1] % 2 != 0 else value[1] + 1
        self["ksize_in"] = [ksize_x, ksize_y]

    def get_ksize(self):
        return self.get("ksize_in", (1, 1))

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image.")
    ksize_in: bpy.props.IntVectorProperty(default=(3, 3), min=1, max=30, size=2, get=get_ksize, set=set_ksize, update=update_node, description="Gaussian kernel size.")
    sigmaX_in: bpy.props.FloatProperty(default=0, min=0, max=255, update=update_node, description="Gaussian kernel standard deviation in X direction.")
    sigmaY_in: bpy.props.FloatProperty(default=0, min=0, max=255, update=update_node, description="Gaussian kernel standard deviation in Y direction.")
    borderType_in: bpy.props.EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=update_node, description="Pixel extrapolation method, see cv::BorderTypes.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('StringsSocket', "sigmaX_in").prop_name = 'sigmaX_in'
        self.inputs.new('StringsSocket', "sigmaY_in").prop_name = 'sigmaY_in'

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("src_in"),
            'ksize_in': self.get_from_props("ksize_in"),
            'sigmaX_in': self.get_from_props("sigmaX_in"),
            'sigmaY_in': self.get_from_props("sigmaY_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        dst_out = self.process_cv(fn=cv2.GaussianBlur, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "borderType_in")
