import uuid

import bpy
import cv2
from ocvl.core.node_base import COLOR_DEPTH_WITH_NONE_ITEMS, OCVLNodeBase, update_node

AUTO_RESIZE_ITEMS = (
    ("OFF", "OFF", "Resize OFF", "", 0),
    ("FIRST", "FIRST", "Resize first", "", 1),
    ("SECOND", "SECOND", "Resize second", "", 2),
)


class OCVLaddWeightedNode(OCVLNodeBase):
    n_doc = "Calculates the weighted sum of two arrays."
    n_note = ""
    n_requirements = {"__and__": ["src1", "src2"]}

    loc_auto_resize: bpy.props.EnumProperty(items=AUTO_RESIZE_ITEMS, default="SECOND", update=update_node, description="Automatic adjust size image.")

    src1_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="First input array.")
    src2_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="Second input array.")
    alpha_in: bpy.props.FloatProperty(default=0.3, min=0.0, max=1.0, step=1,update=update_node, description="Weight of the first array elements.")
    beta_in: bpy.props.FloatProperty(default=0.7, min=0.0, max=1.0, step=1, update=update_node, description="Weight of the second array elements.")
    gamma_in: bpy.props.FloatProperty(default=0.0, min=0.0, max=1.0, step=1, update=update_node, description="Scalar added to each sum.")
    dtype_in: bpy.props.EnumProperty(items=COLOR_DEPTH_WITH_NONE_ITEMS, default='None', update=update_node, description="Desired depth of the destination image, see @ref filter_depths 'combinations'.")

    dst_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.inputs.new("ImageSocket", name="src1", identifier="src1_in")
        self.inputs.new("ImageSocket", name="src2", identifier="src2_in")
        self.inputs.new('StringsSocket', name="alpha_in", identifier="alpha_in").prop_name = 'alpha_in'
        self.inputs.new('StringsSocket', name="beta_in", identifier="beta_in").prop_name = 'beta_in'
        self.inputs.new('StringsSocket', name="gamma_in", identifier="gamma_in").prop_name = 'gamma_in'

        self.outputs.new("ImageSocket", name="dst", identifier="dst_out")

    def wrapped_process(self):
        src1 = self.get_from_props("src1")
        src2 = self.get_from_props("src2")
        dtype_in = self.get_from_props("dtype_in")
        kwargs = {
            'src1': src1 if self.loc_auto_resize != "FIRST" else cv2.resize(src1, src1.shape[::-1][1:]),
            'src2': src2 if self.loc_auto_resize != "SECOND" else cv2.resize(src2, src2.shape[::-1][1:]),
            'alpha': self.get_from_props("alpha_in"),
            'beta': self.get_from_props("beta_in"),
            'gamma': self.get_from_props("gamma_in"),
            'dtype_in': -1 if dtype_in is None else dtype_in
            }

        dst = self.process_cv(fn=cv2.addWeighted, kwargs=kwargs)
        self.refresh_output_socket("dst", dst, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "loc_auto_resize", expand=True)
        self.add_button(layout, "dtype_in", expand=True)
