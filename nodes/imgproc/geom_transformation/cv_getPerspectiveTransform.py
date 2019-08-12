import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLgetPerspectiveTransformNode(OCVLNodeBase):

    n_doc = "Calculates a perspective transform from four pairs of the corresponding points."
    n_requirements = {"__and__": ["src_in"]}
    n_quick_link_requirements = {"src_in":
        {"__type_node__": "OCVLMatNode", "loc_input_mode": "MANUAL", "loc_manual_input": "[[56,65],[368,52],[28,387],[389,390]]", "value_type_in": "float32"}
    }

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Coordinates of quadrangle vertices in the source image.")

    dst_in: bpy.props.StringProperty(name="dst_in", default=str(uuid.uuid4()), description="Coordinates of the corresponding quadrangle vertices in the destination image.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")

        self.outputs.new("OCVLMatrixSocket", "dst_in")

    def wrapped_process(self):
        src_in = self.get_from_props("src_in")
        kwargs = {
            'src_in': src_in,
            'dst_in': src_in.copy(),
        }

        dst_in = self.process_cv(fn=cv2.getPerspectiveTransform, kwargs=kwargs)
        self.refresh_output_socket("dst_in", dst_in, is_uuid_type=True)
