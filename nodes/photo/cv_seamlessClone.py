import uuid

import bpy
import cv2
import numpy as np
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLseamlessCloneNode(OCVLNodeBase):

    n_doc = """
    Image editing tasks concern either global changes (color/intensity corrections, filters, deformations) or local changes concerned to a selection. Here we are interested in achieving local changes, ones that are restricted to a region manually selected (ROI), in a seamless and effortless manner. The extent of the changes ranges from slight distortions to complete replacement by novel content
    """
    bl_flags_list = 'NORMAL_CLONE, MIXED_CLONE, FEATURE_EXCHANGE'

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input 8-bit 3-channel image.")
    dst_in: bpy.props.StringProperty(name="dst_in", default=str(uuid.uuid4()), description="Input 8-bit 3-channel image.")
    mask_in: bpy.props.StringProperty(name="mask_in", default=str(uuid.uuid4()), description="Input 8-bit 1 or 3-channel image.")
    p_in: bpy.props.IntVectorProperty(default=(0, 0), size=2, update=update_node, description="Point in dst image where object is placed.")
    flags_in: bpy.props.BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")), update=update_node, subtype="NONE", description=bl_flags_list)

    result_out: bpy.props.StringProperty(name="result_out", default=str(uuid.uuid4()), description="Output image with the same size and type as dst.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new('ImageSocket', "dst_in")
        self.inputs.new('StringsSocket', "mask_in")
        self.inputs.new('StringsSocket', "p_in").prop_name = 'p_in'

        self.outputs.new("ImageSocket", "result_out")

    def wrapped_process(self):
        self.check_input_requirements(["src_in", "dst_in"])
        src_in = self.get_from_props("src_in")
        kwargs = {
            'src_in': src_in,
            'dst_in': self.get_from_props("dst_in"),
            'mask_in': 255 * np.ones(src_in.shape, src_in.dtype),
            'p_in': self.get_from_props("p_in"),
            'flags_in': self.get_from_props("flags_in"),
            }

        result_out = self.process_cv(fn=cv2.seamlessClone, kwargs=kwargs)
        self.refresh_output_socket("result_out", result_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")
