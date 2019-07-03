import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLrandShuffleNode(OCVLNodeBase):

    n_doc = "Shuffles the array elements randomly."
    n_requirements = {"__and__": ["dst_in"]}

    dst_in: bpy.props.StringProperty(name="dst_in", default=str(uuid.uuid4()),  description="Input/output numerical 1D array.")
    iterFactor_in: bpy.props.FloatProperty(name="iterFactor_in", default=1, min=0, max=100, update=update_node, description="Scale factor that determines the number of random swap operations.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of random numbers; the array must be pre-allocated.")

    def init(self, context):
        self.inputs.new("ImageSocket", "dst_in")
        self.inputs.new("StringsSocket", "iterFactor_in").prop_name = "iterFactor_in"

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'dst_in': self.get_from_props("dst_in").copy(),
            'iterFactor_in': self.get_from_props("iterFactor_in"),
            }

        dst_out = self.process_cv(fn=cv2.randShuffle, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
