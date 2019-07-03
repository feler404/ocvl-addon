import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLsortNode(OCVLNodeBase):
    bl_flags_list = 'SORT_EVERY_ROW, SORT_EVERY_COLUMN, SORT_ASCENDING, SORT_DESCENDING'

    n_doc = "Sorts each row or each column of a matrix."
    n_requirements = {"__and__": ["src_in"]}
    n_quick_link_requirements = {"src_in": {"code_in": "COLOR_BGR2GRAY"}}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()),  description="Input single-channel array.")
    flags_in: bpy.props.BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")), update=update_node, subtype="NONE", description=bl_flags_list)

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output solution.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'flags_in': self.get_from_props("flags_in"),
            }

        dst_out = self.process_cv(fn=cv2.sort, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")
