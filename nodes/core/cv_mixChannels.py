import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLmixChannelsNode(OCVLNodeBase):

    n_doc = "Copies specified channels from input arrays to the specified channels of output arrays."
    n_requirements = {"__and__": ["src_in", "fromTo_in"]}
    n_quick_link_requirements = {"fromTo_in": {"loc_input_mode": "MANUAL", "loc_manual_input": "[0,2, 1,1, 2,0]"}}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array or vector of matrices; all of the matrices must have the same size and the same depth.")
    fromTo_in: bpy.props.StringProperty(name="fromTo_in", default=str(uuid.uuid4()), description="Array of index pairs specifying which channels are copied and where.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array or vector of matrices.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new("VectorSocket", "fromTo_in")

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        src_in = self.get_from_props("src_in")
        dst_in = src_in.copy()
        kwargs = {
            'src_in': [src_in],
            'dst_in': [dst_in],
            'fromTo_in': [int(i) for i in self.get_from_props("fromTo_in")],
            }

        dst_out = self.process_cv(fn=cv2.mixChannels, kwargs=kwargs)[0]
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
