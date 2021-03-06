import bpy

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLPointNode(OCVLNodeBase):

    n_doc = "Point."

    x_in: bpy.props.IntProperty(default=10, min=0, max=2048, update=update_node, description="X")
    y_in: bpy.props.IntProperty(default=10, min=0, max=2048, update=update_node, description="Y")

    def init(self, context):
        self.inputs.new("OCVLObjectSocket", "x_in").prop_name = "x_in"
        self.inputs.new("OCVLObjectSocket", "y_in").prop_name = "y_in"
        self.outputs.new("OCVLObjectSocket", "point_out")

    def wrapped_process(self):
        x_in = self.get_from_props("x_in")
        y_in = self.get_from_props("y_in")

        point_out = x_in, y_in
        self.refresh_output_socket("point_out", point_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass
