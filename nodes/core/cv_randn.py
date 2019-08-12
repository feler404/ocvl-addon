import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLrandnNode(OCVLNodeBase):

    n_doc = "Fills the array with normally distributed random numbers."
    n_requirements = {"__and__": ["dst_in"]}

    dst_in: bpy.props.StringProperty(name="dst_in", default=str(uuid.uuid4()),  description="Output array of random numbers; the array must be pre-allocated.")
    mean_in: bpy.props.IntProperty(name="mean_in", default=100, min=0, max=1000, update=update_node, description="Mean value (expectation) of the generated random numbers.")
    stddev_in: bpy.props.IntProperty(name="stddev_in", default=50, min=0, max=1000, update=update_node, description="Standard deviation of the generated random numbers.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of random numbers; the array must be pre-allocated.")

    def init(self, context):
        self.inputs.new("OCVLObjectSocket", "mean_in").prop_name = "mean_in"
        self.inputs.new("OCVLObjectSocket", "stddev_in").prop_name = "stddev_in"
        self.inputs.new("OCVLImageSocket", "dst_in")

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'mean_in': self.get_from_props("mean_in"),
            'stddev_in': self.get_from_props("stddev_in"),
            'dst_in': self.get_from_props("dst_in").copy(),
            }

        dst_out = self.process_cv(fn=cv2.randn, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
