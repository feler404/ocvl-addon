import uuid

import bpy
from ocvl.core.node_base import OCVLNodeBase, update_node
from ocvl.core.settings import STETHOSCOPE_NODE_MAX_LINES, WRAP_TEXT_SIZE_FOR_ERROR_DISPLAY


class OCVLStethoscopeNode(OCVLNodeBase):

    n_doc = "Stethoscope"
    n_requirements = {"__and__": ["matrix_in"]}

    matrix_in: bpy.props.StringProperty(name="matrix_in", default=str(uuid.uuid4()))

    def init(self, context):
        self.width = 200
        self.inputs.new("StringsSocket", "matrix_in")

    def wrapped_process(self):
        pass

    def draw_buttons(self, context, layout):
        matrix_in = self.get_from_props("matrix_in")
        lines = str(matrix_in).split("\n")
        for i, line in enumerate(lines):
            if i > STETHOSCOPE_NODE_MAX_LINES:
                layout.label(text="...")
                break
            layout.label(text=str(line)[:WRAP_TEXT_SIZE_FOR_ERROR_DISPLAY])
