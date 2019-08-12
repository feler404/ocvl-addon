import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, COLOR_DEPTH_ITEMS, BORDER_TYPE_ITEMS


class OCVLLaplacianNode(OCVLNodeBase):

    n_doc = "Calculates the Laplacian of an image."
    n_requirements = {"__and__": ["src_in"]}

    def set_ksize(self, value):
        if value % 2 == 0:
            value = value + 1
        self["ksize_in"] = value

    def get_ksize(self):
        return self.get("ksize_in", 1)

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image.")
    ddepth_in: bpy.props.EnumProperty(items=COLOR_DEPTH_ITEMS, default='CV_8U', update=update_node, description="Desired depth of the destination image.")
    ksize_in: bpy.props.IntProperty(default=1, update=update_node, min=1, max=10, set=set_ksize, get=get_ksize, description="Aperture size used to compute the second-derivative filters.")
    scale_in: bpy.props.FloatProperty(default=1.0, min=1, max=8, update=update_node, description="Optional scale factor for the computed Laplacian values.")
    delta_in: bpy.props.FloatProperty(default=0.0, min=0, max=255, update=update_node, description="Optional delta value that is added to the results prior to storing them in dst.")
    borderType_in: bpy.props.EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=update_node, description="Pixel extrapolation method, see cv::BorderTypes.")
    
    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new('OCVLObjectSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('OCVLObjectSocket', "scale_in").prop_name = 'scale_in'
        self.inputs.new('OCVLObjectSocket', "delta_in").prop_name = 'delta_in'

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'ddepth_in': self.get_from_props("ddepth_in"),
            'ksize_in': int(self.get_from_props("ksize_in")),
            'scale_in': self.get_from_props("scale_in"),
            'delta_in': self.get_from_props("delta_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        dst_out = self.process_cv(fn=cv2.Laplacian, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')
        self.add_button(layout, 'ddepth_in')
