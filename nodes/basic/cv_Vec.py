import uuid

import bpy
import numpy as np
from ocvl.core.constants import NP_VALUE_TYPE_ITEMS
from ocvl.core.node_base import OCVLNodeBase, update_node

VEC_MODE_ITEMS = (
    ("ZEROS", "ZEROS", "ZEROS", "", 0),
    ("ONES", "ONES", "ONES", "", 1),
    ("RANDOM", "RANDOM", "RANDOM", "", 2),
    ("MANUAL", "MANUAL", "MANUAL", "", 3),
)

PROPS_MAPS = {
    VEC_MODE_ITEMS[0][0]: ("size_in", "value_type_in"),
    VEC_MODE_ITEMS[1][0]: ("size_in", "value_type_in"),
    VEC_MODE_ITEMS[2][0]: ("size_in", "value_type_in"),
    VEC_MODE_ITEMS[3][0]: ("value_type_in", "loc_manual_input"),
}


class OCVLVecNode(OCVLNodeBase):

    n_doc = "Vector."

    def update_layout(self, context):
        self.update_sockets(context)
        update_node(self, context)

    size_in: bpy.props.IntProperty(default=10, min=1, max=2048, update=update_node, description="Size of vector")
    value_type_in: bpy.props.EnumProperty(items=NP_VALUE_TYPE_ITEMS, default='uint8', update=update_node, description="Data type.")
    loc_input_mode: bpy.props.EnumProperty(items=VEC_MODE_ITEMS, default='RANDOM', update=update_layout, description="Data type.")
    loc_manual_input: bpy.props.StringProperty(default='[0, 1, 2]', maxlen=1024, update=update_node)

    vector_out: bpy.props.StringProperty(default=str(uuid.uuid4()))

    def init(self, context):
        self.width = 250
        self.inputs.new("OCVLObjectSocket", "size_in").prop_name = "size_in"

        self.outputs.new("OCVLVectorSocket", "vector_out")
        self.update_layout(context)

    def wrapped_process(self):
        size_in = self.get_from_props("size_in")
        loc_input_mode = self.get_from_props("loc_input_mode")
        value_type_in = self.get_from_props("value_type_in")
        dtype = np.uint8 if value_type_in == "NONE" else getattr(np, value_type_in)

        if loc_input_mode == "ZEROS":
            vector_out = np.zeros(size_in, dtype=dtype)
        elif loc_input_mode == "ONES":
            vector_out = np.ones(size_in, dtype=dtype)
        elif loc_input_mode == "MANUAL":
            loc_manual_input = self.get_from_props("loc_manual_input")
            try:
                eval_list = eval(loc_manual_input)
                if isinstance(eval_list, tuple):
                    vector_out = eval_list
                else:
                    vector_out = np.array(eval_list, dtype=dtype)
            except Exception as e:
                self.n_errors = "Evaluation error. Details: {}".format(e)
                vector_out = []
        else:
            vector_out = np.array(np.random.random_sample(size_in) * 255)
            vector_out = vector_out.astype(dtype)

        self.refresh_output_socket("vector_out", vector_out, is_uuid_type=True)

    def update_sockets(self, context):
        self.update_sockets_for_node_mode(PROPS_MAPS, self.loc_input_mode)
        self.process()

    def draw_buttons(self, context, layout):
        self.add_button(layout, "loc_input_mode", expand=True)
