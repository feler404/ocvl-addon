import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLcompleteSymmNode(OCVLNodeBase):

    n_doc = "Copies the lower or the upper half of a square matrix to another half."
    n_requirements = {"__and__": ["m_in"]}
    n_input_output_only = True

    m_in: bpy.props.StringProperty(name="m_in", default=str(uuid.uuid4()), description="Input-output floating-point square matrix.")

    lowerToUpper_in: bpy.props.BoolProperty(name="lowerToUpper_in", default=False, update=update_node, description="Operation flag; if true, the lower half is copied to the upper half. Otherwise, the upper half is copied to the lower half.")
    m_out: bpy.props.StringProperty(name="m_out", default=str(uuid.uuid4()), description="Input-output floating-point square matrix.")

    def init(self, context):
        self.inputs.new("ImageSocket", "m_in")

        self.outputs.new("ImageSocket", "m_out")

    def wrapped_process(self):
        kwargs = {
            'm_in': self.get_from_props("m_in"),
            'lowerToUpper_in': self.get_from_props("lowerToUpper_in"),
            }

        m_out = self.get_from_props("m_in")
        _ = self.process_cv(fn=cv2.completeSymm, kwargs=kwargs)
        self.refresh_output_socket("m_out", m_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "lowerToUpper_in")