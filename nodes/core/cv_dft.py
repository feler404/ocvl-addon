import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLdftNode(OCVLNodeBase):

    bl_flags_list = 'DFT_INVERSE, DFT_SCALE, DFT_ROWS, DFT_COMPLEX_OUTPUT, DFT_REAL_OUTPUT'

    n_requirements = {"__and__": ["src_in"]}
    n_doc = "Performs a forward or inverse Discrete Fourier transform of a 1D or 2D floating-point array."
    n_quick_link_requirements = {"src_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"}}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array that could be real or complex.")
    flags_in: bpy.props.BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")), update=update_node, subtype="NONE", description=bl_flags_list)
    nonzeroRows_in: bpy.props.IntProperty(default=0, min=0, update=update_node, description="When the parameter is not zero, the function assumes that only the first nonzeroRows rows of the input array (DFT_INVERSE is not set) or only the first nonzeroRows of the output array (DFT_INVERSE is set) contain non-zeros.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array whose size and type depends on the flags.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLObjectSocket", "nonzeroRows_in").prop_name = "nonzeroRows_in"

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):

        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'nonzeroRows_in': self.get_from_props("nonzeroRows_in"),
            'flags_in': self.get_from_props("flags_in"),
            }

        dst_out = self.process_cv(fn=cv2.dft, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")
