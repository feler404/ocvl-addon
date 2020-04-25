import uuid

import bpy
import cv2
from ocvl_addon.core.node_base import OCVLNodeBase, update_node, SUFFIX_COLLECTION_NAMES


class OCVLcvtColorNode(OCVLNodeBase):

    bl_icon = 'COLOR'

    n_doc = "Converts an image from one color space to another."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image: 8-bit unsigned, 16-bit unsigned ( CV_16UC... ), or single-precision floating-point.")
    dstCn_in: bpy.props.IntProperty(default=0, update=update_node, min=0, max=4, description="Number of channels in the destination image; if the parameter is 0, the number of the channels is derived automatically from input image and code.")

    code_in: bpy.props.StringProperty(name="code_in", default='COLOR_BGR2GRAY', update=update_node, description="Color space conversion code (see cv::ColorConversionCodes).")
    code_in_names: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image of the same size and depth as input image.")

    def init(self, context):
        self.width = 300
        self.render_collection_names("code_in", "COLOR_")
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLObjectSocket", "dstCn_in").prop_name = "dstCn_in"

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in"])

        kwargs = {
            'src': self.get_from_props("src_in"),
            'code_in': self.get_from_props("code_in"),
            'dstCn_in': self.get_from_props("dstCn_in"),
            }

        dst_out = self.process_cv(fn=cv2.cvtColor, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        prop_search_name = "code_in"
        row.prop_search(self, prop_search_name, self, f"{prop_search_name}_{SUFFIX_COLLECTION_NAMES}")
