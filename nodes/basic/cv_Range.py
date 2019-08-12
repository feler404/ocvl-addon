import bpy

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLRangeNode(OCVLNodeBase):

    n_doc = "Range."

    start_in: bpy.props.IntProperty(default=10, min=0, update=update_node, description="Start input.")
    end_in: bpy.props.IntProperty(default=10, min=0, update=update_node, description="End input.")

    def init(self, context):
        self.inputs.new("OCVLMatrixSocket", "start_in").prop_name = "start_in"
        self.inputs.new("OCVLMatrixSocket", "end_in").prop_name = "end_in"
        self.outputs.new("OCVLMatrixSocket", "range_out")

    def wrapped_process(self):
        start_in = self.get_from_props("start_in")
        end_in = self.get_from_props("end_in")

        range_out = list(range(start_in, end_in))
        self.refresh_output_socket("range_out", range_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass
