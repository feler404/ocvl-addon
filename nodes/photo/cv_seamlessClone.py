import uuid

import bpy
import cv2
import numpy as np
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLseamlessCloneNode(OCVLNodeBase):

    bl_flags_list = 'NORMAL_CLONE, MIXED_CLONE, FEATURE_EXCHANGE'

    n_doc = "Image editing tasks concern either global changes (color/intensity corrections, filters, deformations) or local changes concerned to a selection. Here we are interested in achieving local changes, ones that are restricted to a region manually selected (ROI), in a seamless and effortless manner. The extent of the changes ranges from slight distortions to complete replacement by novel content"
    n_quick_link_requirements = {"src_in": {"width_in": 100, "height_in": 100}, "dst_in": {"width_in": 300, "height_in": 300}}
    n_requirements = {"__and__": ["src_in", "dst_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input 8-bit 3-channel image.")
    dst_in: bpy.props.StringProperty(name="dst_in", default=str(uuid.uuid4()), description="Input 8-bit 3-channel image.")
    mask_in: bpy.props.StringProperty(name="mask_in", default=str(uuid.uuid4()), description="Input 8-bit 1 or 3-channel image.")
    p_in: bpy.props.IntVectorProperty(default=(50, 50), size=2, update=update_node, description="Point in dst image where object is placed.")
    flags_in: bpy.props.BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")), update=update_node, subtype="NONE", description=bl_flags_list)

    result_out: bpy.props.StringProperty(name="result_out", default=str(uuid.uuid4()), description="Output image with the same size and type as dst.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new('OCVLImageSocket', "dst_in")
        self.inputs.new('OCVLMaskSocket', "mask_in")
        self.inputs.new('OCVLObjectSocket', "p_in").prop_name = 'p_in'

        self.outputs.new("OCVLImageSocket", "result_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'dst_in': self.get_from_props("dst_in"),
            'mask_in': self.get_from_props("mask_in"),
            'p_in': self.get_from_props("p_in"),
            'flags_in': self.get_from_props("flags_in"),
            }

        if isinstance(kwargs['mask_in'], str) and isinstance(kwargs['src_in'], np.ndarray):
            kwargs['mask_in'] = 255 * np.ones(kwargs['src_in'].shape, kwargs['src_in'].dtype)

        result_out = self.process_cv(fn=cv2.seamlessClone, kwargs=kwargs)
        self.refresh_output_socket("result_out", result_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")
