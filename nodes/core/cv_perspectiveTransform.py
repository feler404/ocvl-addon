import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase


class OCVLperspectiveTransformNode(OCVLNodeBase):

    n_doc = "Performs the perspective matrix transformation of vectors."
    n_requirements = {"__and__": ["src_in", "m_in"]}
    n_quick_link_requirements = {
        "src_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
        "m_in": {"__type_node__": "OCVLMatNode", "loc_input_mode": "MANUAL", "loc_manual_input": "[[0, 1], [2, 10]]"}
    }

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input two-channel or three-channel floating-point array; each element is a 2D/3D vector to be transformed.")
    m_in: bpy.props.StringProperty(name="m_in", default=str(uuid.uuid4()), description="3x3 or 4x4 floating-point transformation matrix.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same size and type as src.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new("ImageSocket", "m_in")
        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'm_in': self.get_from_props("m_in"),
            }

        dst_out = self.process_cv(fn=cv2.perspectiveTransform, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
