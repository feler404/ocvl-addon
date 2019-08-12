import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLmulSpectrumsNode(OCVLNodeBase):

    bl_flags_list = 'DFT_ROWS'

    n_doc = "Performs the per-element multiplication of two Fourier spectrums."
    n_requirements = {"__and__": ["a_in", "b_in"]}
    n_quick_link_requirements = {
        "a_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
        "b_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
    }

    a_in: bpy.props.StringProperty(name="a_in", default=str(uuid.uuid4()), description="First input array.")
    b_in: bpy.props.StringProperty(name="b_in", default=str(uuid.uuid4()), description="Second input array of the same size and type as src1.")
    flags_in: bpy.props.BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")), update=update_node, subtype="NONE", description=bl_flags_list)
    conjB_in: bpy.props.BoolProperty(name="conjB_in", default=False, description = "Optional flag that conjugates the second input array before the multiplication (true) or not (false).")

    c_out: bpy.props.StringProperty(name="c_out", default=str(uuid.uuid4()), description="Output array.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "a_in")
        self.inputs.new("OCVLImageSocket", "b_in")

        self.outputs.new("OCVLImageSocket", "c_out")

    def wrapped_process(self):
        kwargs = {
            'a_in': self.get_from_props("a_in"),
            'b_in': self.get_from_props("b_in"),
            'flags_in': self.get_from_props("flags_in"),
            'conjB_in': self.get_from_props("conjB_in"),
            }

        c_out = self.process_cv(fn=cv2.mulSpectrums, kwargs=kwargs)
        self.refresh_output_socket("c_out", c_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")
        self.add_button(layout, "conjB_in")
