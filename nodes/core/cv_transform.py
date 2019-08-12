import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, NORMALIZATION_TYPE_ITEMS, COLOR_DEPTH_WITH_NONE_ITEMS


class OCVLtransformNode(OCVLNodeBase):

    n_doc = "Performs the matrix transformation of every array element."
    n_requirements = {"__and__": ["src_in", "m_in"]}
    n_quick_link_requirements = {
        "src_in": {"code_in": "COLOR_BGR2GRAY"},
        "m_in": {"__type_node__": "OCVLMatNode", "loc_input_mode": "MANUAL", "loc_manual_input": "[[0, 50], [1, 20], [1, 20]]"}
    }

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array that must have as many channels (1 to 4) as m.cols or m.cols-1.")
    m_in: bpy.props.StringProperty(name="m_in", default=str(uuid.uuid4()), description="Transformation 2x2 or 2x3 floating-point matrix.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same size and depth as src; it has as many channels as m.rows.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLImageSocket", "m_in")

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'm_in': self.get_from_props("m_in"),
            }

        dst_out = self.process_cv(fn=cv2.transform, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
