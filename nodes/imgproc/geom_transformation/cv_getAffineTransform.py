import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLgetAffineTransformNode(OCVLNodeBase):

    n_doc = "Calculates an affine transform from three pairs of the corresponding points."
    n_requirements = {"__and__": ["src_in"]}
    n_quick_link_requirements = {"src_in":
        {"__type_node__": "OCVLMatNode", "loc_input_mode": "MANUAL", "loc_manual_input": "[[0, 0], [1, 1], [3,2]]", "value_type_in": "float32"}
    }
    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Coordinates of triangle vertices in the source image.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output matrix.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")

        self.outputs.new("OCVLObjectSocket", "dst_out")

    def wrapped_process(self):
        src_in = self.get_from_props("src_in")
        kwargs = {
            'src': self.get_from_props("src_in"),
            'dst': src_in.copy(),
        }

        dst_out = self.process_cv(fn=cv2.getAffineTransform, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
