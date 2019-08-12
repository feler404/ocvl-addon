import bpy
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLFloatNode(OCVLNodeBase):

    n_doc = "Single integer number from Python interface perspective."

    float_out: bpy.props.FloatProperty(default=0.1, min=0, max=1, step=1, precision=4, update=update_node, description="Simple integer number.")

    def init(self, context):
        self.outputs.new("OCVLObjectSocket", "float_out")

    def wrapped_process(self):
        self.refresh_output_socket("float_out", self.float_out)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "float_out")

    def refresh_output_socket(self, prop_name=None, prop_value=None):
        # we need overload this method to prevent infinite recursion
        self.outputs[prop_name].sv_set([[prop_value]])