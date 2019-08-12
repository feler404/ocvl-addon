import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLranduNode(OCVLNodeBase):

    n_doc = "Generates a single uniformly-distributed random number or an array of random numbers."
    n_requirements = {"__and__": ["dst_in"]}
    n_quick_link_requirements = {"dst_in": {"code_in": "COLOR_BGR2GRAY"}}

    dst_in: bpy.props.StringProperty(name="dst_in", default=str(uuid.uuid4()),  description="Output array of random numbers; the array must be pre-allocated.")
    low_in: bpy.props.IntProperty(name="low_in", default=0, min=0, max=1000, update=update_node, description="Inclusive lower boundary of the generated random numbers.")
    high_in: bpy.props.IntProperty(name="high_in", default=255, min=0, max=1000, update=update_node, description="Exclusive upper boundary of the generated random numbers.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of random numbers; the array must be pre-allocated.")

    def init(self, context):
        self.inputs.new("OCVLMatrixSocket", "low_in").prop_name = "low_in"
        self.inputs.new("OCVLMatrixSocket", "high_in").prop_name = "high_in"
        self.inputs.new("OCVLImageSocket", "dst_in")

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'low_in': self.get_from_props("low_in"),
            'high_in': self.get_from_props("high_in"),
            'dst_in': self.get_from_props("dst_in").copy(),
            }

        dst_out = self.process_cv(fn=cv2.randu, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
