import uuid

import bpy
import cv2
from ocvl_addon.core.node_base import OCVLNodeBase, update_node


class OCVLfastNlMeansDenoisingNode(OCVLNodeBase):

    n_doc = "Modification of fastNlMeansDenoising function for colored images."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), update=update_node, description="Input 8-bit 3-channel image.")
    templateWindowSize_in: bpy.props.IntProperty(name="templateWindowSize_in", default=7, min=1, max=124, update=update_node, description="Size in pixels of the template patch that is used to compute weights. Should be odd. Recommended value 7 pixels.")
    searchWindowSize_in: bpy.props.IntProperty(name="searchWindowSize_in", default=21, min=1, max=124, update=update_node, description="Size in pixels of the window that is used to compute weighted average for given pixel. Should be odd. Affect performance linearly: greater searchWindowsSize - greater denoising time. Recommended value 21 pixels.")
    h_in: bpy.props.IntProperty(name="h_in", default=3, min=1, max=128, update=update_node, description="Parameter regulating filter strength for luminance component. Bigger h value perfectly removes noise but also removes image details, smaller h value preserves details but also preserves some noise.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image with the same size and type as src .")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLObjectSocket", "templateWindowSize_in").prop_name = "templateWindowSize_in"
        self.inputs.new("OCVLObjectSocket", "searchWindowSize_in").prop_name = "searchWindowSize_in"
        self.inputs.new("OCVLObjectSocket", "h_in").prop_name = "h_in"

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'templateWindowSize_in': self.get_from_props("templateWindowSize_in"),
            'searchWindowSize_in': self.get_from_props("searchWindowSize_in"),
            'h_in': self.get_from_props("h_in"),
        }

        dst_out = self.process_cv(fn=cv2.fastNlMeansDenoising, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
