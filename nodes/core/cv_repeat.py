import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLrepeatNode(OCVLNodeBase):

    n_doc = "Fills the output array with repeated copies of the input array."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()),  description="Input array to replicate.")
    nx_in: bpy.props.IntProperty(name="nx_in", default=3, min=1, max=20, update=update_node, description="Flag to specify how many times the src is repeated along the horizontal axis.")
    ny_in: bpy.props.IntProperty(name="ny_in", default=3, min=1, max=20, update=update_node, description="Flag to specify how many times the src is repeated along the vertical axis.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same type as src.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new("StringsSocket", "nx_in").prop_name = "nx_in"
        self.inputs.new("StringsSocket", "ny_in").prop_name = "ny_in"

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'nx_in': self.get_from_props("nx_in"),
            'ny_in': self.get_from_props("ny_in"),
            }

        dst_out = self.process_cv(fn=cv2.repeat, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
