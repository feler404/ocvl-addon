import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLsolveNode(OCVLNodeBase):

    bl_flags_list = 'DECOMP_LU, DECOMP_CHOLESKY, DECOMP_EIG, DECOMP_SVD, DECOMP_QR, DECOMP_NORMAL'

    n_doc = "Solves one or more linear systems or least-squares problems."
    n_requirements = {"__and__": ["src1_in", "src2_in"]}
    n_quick_link_requirements = {
        "src1_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32", "width_in": 5, "height_in": 5},
        "src2_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32", "width_in": 5, "height_in": 5},
    }

    src1_in: bpy.props.StringProperty(name="src1_in", default=str(uuid.uuid4()),  description="Input matrix on the left-hand side of the system.")
    src2_in: bpy.props.StringProperty(name="src2_in", default=str(uuid.uuid4()),  description="Input matrix on the right-hand side of the system.")
    flags_in: bpy.props.BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")), update=update_node, subtype="NONE", description=bl_flags_list)

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output solution.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src1_in")
        self.inputs.new("OCVLImageSocket", "src2_in")

        self.outputs.new("OCVLMatrixSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src1_in': self.get_from_props("src1_in"),
            'src2_in': self.get_from_props("src2_in"),
            'flags_in': self.get_from_props("flags_in"),
            }

        dst_out = self.process_cv(fn=cv2.solve, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")
