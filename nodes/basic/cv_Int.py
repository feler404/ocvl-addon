import bpy
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLIntNode(OCVLNodeBase):

    n_doc = "Single integer number from Python interface perspective."

    int_out: bpy.props.IntProperty(default=1, min=0, step=1, update=update_node, description="Simple integer number.")

    def init(self, context):
        self.outputs.new("OCVLObjectSocket", "int_out")

    def wrapped_process(self):
        self.refresh_output_socket("int_out", self.int_out)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "int_out")

    def refresh_output_socket(self, prop_name=None, prop_value=None):
        # we need overload this method to prevent infinite recursion
        self.outputs[prop_name].sv_set([[prop_value]])