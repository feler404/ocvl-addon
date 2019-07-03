import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node, REDUCE_TYPES_ITEMS


class OCVLsetIdentityNode(OCVLNodeBase):

    n_doc = "Initializes a scaled identity matrix."
    n_requirements = {"__and__": ["mtx_in"]}

    mtx_in: bpy.props.StringProperty(name="mtx_in", default=str(uuid.uuid4()),  description="Matrix to initialize (not necessarily square).")
    s_in: bpy.props.IntProperty(name="s_in", default=150, min=0, max=255, update=update_node, description="Value to assign to diagonal elements.")

    mtx_out: bpy.props.StringProperty(name="mtx_out", default=str(uuid.uuid4()), description="Output array of the same type as mtx.")

    def init(self, context):
        self.inputs.new("ImageSocket", "mtx_in")
        self.inputs.new("StringsSocket", "s_in").prop_name = "s_in"

        self.outputs.new("ImageSocket", "mtx_out")

    def wrapped_process(self):
        kwargs = {
            'mtx_in': self.get_from_props("mtx_in"),
            's_in': self.get_from_props("s_in"),
            }

        mtx_out = self.process_cv(fn=cv2.setIdentity, kwargs=kwargs)
        self.refresh_output_socket("mtx_out", mtx_out, is_uuid_type=True)
