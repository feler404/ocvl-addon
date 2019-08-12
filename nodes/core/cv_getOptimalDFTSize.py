import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLgetOptimalDFTSizeNode(OCVLNodeBase):

    n_doc = "Returns the optimal DFT size for a given vector size."

    vecsize_in: bpy.props.IntProperty(name="vecsize_in", update=update_node, default=10, description="Vector size..")

    retval_out: bpy.props.IntProperty(name="retval_out", default=0, description="The function returns a negative number if vecsize is too large (very close to INT_MAX ).")

    def init(self, context):
        self.inputs.new("OCVLMatrixSocket", "vecsize_in").prop_name = "vecsize_in"
        self.outputs.new("OCVLMatrixSocket", "retval_out")

    def wrapped_process(self):

        kwargs = {
            'vecsize': self.get_from_props("vecsize_in"),
            }

        retval_out = self.process_cv(fn=cv2.getOptimalDFTSize, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out)
