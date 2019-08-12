import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, NORMALIZATION_TYPE_ITEMS, COLOR_DEPTH_WITH_NONE_ITEMS


class OCVLtraceNode(OCVLNodeBase):

    n_doc = "Returns the trace of a matrix."
    n_requirements = {"__and__": ["mtx_in"]}

    mtx_in: bpy.props.StringProperty(name="mtx_in", default=str(uuid.uuid4()), description="Input matrix.")

    retval_out: bpy.props.StringProperty(name="retval_out", default=str(uuid.uuid4()), description="Output.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "mtx_in")

        self.outputs.new("OCVLObjectSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'mtx_in': self.get_from_props("mtx_in"),
            }

        retval_out = self.process_cv(fn=cv2.trace, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)
