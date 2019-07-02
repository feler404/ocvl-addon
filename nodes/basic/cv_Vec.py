import bpy
import uuid
import numpy as np

from ocvl.core.node_base import OCVLNodeBase, update_node
from ocvl.core.constants import NP_VALUE_TYPE_ITEMS


VEC_MODE_ITEMS = {
    ("ZEROS", "ZEROS", "ZEROS", "", 0),
    ("ONES", "ONES", "ONES", "", 1),
    ("RANDOM", "RANDOM", "RANDOM", "", 2),
}


class OCVLVecNode(OCVLNodeBase):

    n_doc = "Vector."

    size_in: bpy.props.IntProperty(default=10, min=1, max=2048, update=update_node, description="Size of vector")
    value_type_in: bpy.props.EnumProperty(items=NP_VALUE_TYPE_ITEMS, default='uint8', update=update_node, description="Data type.")
    loc_mode: bpy.props.EnumProperty(items=VEC_MODE_ITEMS, default='RANDOM', update=update_node, description="Data type.")

    vector_out: bpy.props.StringProperty(default=str(uuid.uuid4()))

    def init(self, context):
        self.inputs.new("StringsSocket", "size_in").prop_name = "size_in"
        self.inputs.new("StringsSocket", "value_type_in").prop_name = "value_type_in"
        self.outputs.new("VectorSocket", "vector_out")

    def wrapped_process(self):
        size_in = self.get_from_props("size_in")
        loc_mode = self.get_from_props("loc_mode")
        value_type_in = self.get_from_props("value_type_in")
        dtype = np.uint8 if value_type_in == "NONE" else getattr(np, value_type_in)

        if loc_mode == "ZEROS":
            vector_out = np.zeros(size_in, dtype=dtype)
        elif loc_mode == "ONES":
            vector_out = np.ones(size_in, dtype=dtype)
        else:
            vector_out = np.array([int(element)for element in np.random.random_sample(size_in) * 255])
            vector_out.astype(dtype)

        self.refresh_output_socket("vector_out", vector_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "loc_mode", expand=True)
