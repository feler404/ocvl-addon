from bpy.props import IntProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLRangeNode(OCVLNode):
    start_in = IntProperty(default=10, min=0, update=updateNode)
    end_in = IntProperty(default=10, min=0, update=updateNode)

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "start_in").prop_name = "start_in"
        self.inputs.new("StringsSocket", "end_in").prop_name = "end_in"
        self.outputs.new("StringsSocket", "range_out")

    def wrapped_process(self):
        start_in = self.get_from_props("start_in")
        end_in = self.get_from_props("end_in")

        range_out = list(range(start_in, end_in))
        self.refresh_output_socket("range_out", range_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLRangeNode)


def unregister():
    cv_unregister_class(OCVLRangeNode)
