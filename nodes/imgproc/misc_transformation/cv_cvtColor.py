import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, CODE_COLOR_POOR_ITEMS


class OCVLcvtColorNode(OCVLNodeBase):

    bl_icon = 'COLOR'

    n_doc = "Converts an image from one color space to another."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image: 8-bit unsigned, 16-bit unsigned ( CV_16UC... ), or single-precision floating-point.")
    code_in: bpy.props.EnumProperty(items=CODE_COLOR_POOR_ITEMS, default='COLOR_BGR2GRAY', update=update_node, description="Color space conversion code (see cv::ColorConversionCodes).")
    dstCn_in: bpy.props.IntProperty(default=0, update=update_node, min=0, max=4, description="Number of channels in the destination image; if the parameter is 0, the number of the channels is derived automatically from input image and code.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image of the same size and depth as input image.")

    def init(self, context):
        self.width = 200
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new("StringsSocket", "code_in").prop_name = "code_in"
        self.inputs.new("StringsSocket", "dstCn_in").prop_name = "dstCn_in"

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in"])

        kwargs = {
            'src': self.get_from_props("src_in"),
            'code_in': self.get_from_props("code_in"),
            'dstCn_in': self.get_from_props("dstCn_in"),
            }

        dst_out = self.process_cv(fn=cv2.cvtColor, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
