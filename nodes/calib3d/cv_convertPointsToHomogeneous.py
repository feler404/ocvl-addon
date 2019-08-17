import uuid

import bpy
import cv2
import numpy as np
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLconvertPointsToHomogeneousNode(OCVLNodeBase):

    n_doc = "Converts points from Euclidean to homogeneous space."
    n_requirements = {"__and__": ["src_in"]}
    n_quick_link_requirements = {"src_in": {"loc_input_mode": "MANUAL", "value_type_in": "float32", "loc_manual_input": "[[[0, 0, 1]], [[1, 1, 1]], [[2, 2, 1]]]"}}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input vector of N-dimensional points.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output vector of N+1-dimensional points.")

    def init(self, context):
        self.inputs.new("OCVLVectorSocket", "src_in")

        self.outputs.new("OCVLObjectSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
        }

        dst_out= self.process_cv(fn=cv2.convertPointsToHomogeneous, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)