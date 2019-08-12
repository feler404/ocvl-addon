import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, COLOR_DEPTH_ITEMS, BORDER_TYPE_ITEMS


class OCVLboxFilterNode(OCVLNodeBase):

    bl_icon = 'FILTER'

    n_doc = "Blurs an image using the box filter."
    n_requirements = {"__and__": ["src_in"]}

    def get_anchor(self):
        return self.get("anchor_in", (-1, -1))

    def set_anchor(self, value):
        anchor_x = value[0] if -1 <= value[0] < self.ksize_in[0] else self.anchor_in[0]
        anchor_y = value[1] if -1 <= value[1] < self.ksize_in[1] else self.anchor_in[1]
        self["anchor_in"] = (anchor_x, anchor_y)

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image.")
    ksize_in: bpy.props.IntVectorProperty(default=(3, 3), min=1, max=30, size=2, update=update_node, description="Blurring kernel size.")
    anchor_in: bpy.props.IntVectorProperty(default=(-1, -1), min=-1, max=30, update=update_node, get=get_anchor, set=set_anchor, size=2, description="Anchor point.")
    ddepth_in: bpy.props.EnumProperty(items=COLOR_DEPTH_ITEMS, default='CV_8U', update=update_node, description="The output image depth.")
    normalize_in: bpy.props.BoolProperty(default=True, update=update_node, description="Flag, specifying whether the kernel is normalized by its area or not.")
    borderType_in: bpy.props.EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=update_node, description="Pixel extrapolation method, see cv::BorderTypes")

    dst_in: bpy.props.StringProperty(name="dst_in", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.width = 260
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new('OCVLObjectSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('OCVLObjectSocket', "anchor_in").prop_name = 'anchor_in'

        self.outputs.new("OCVLImageSocket", "dst_in")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'ksize_in': self.get_from_props("ksize_in"),
            'anchor_in': self.get_from_props("anchor_in"),
            'ddepth_in': self.get_from_props("ddepth_in"),
            'normalize_in': self.get_from_props("normalize_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        dst_in = self.process_cv(fn=cv2.boxFilter, kwargs=kwargs)
        self.refresh_output_socket("dst_in", dst_in, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "ddepth_in")
        self.add_button(layout, "normalize_in")
        self.add_button(layout, "borderType_in")
