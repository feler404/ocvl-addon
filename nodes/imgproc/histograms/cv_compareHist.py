import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase

from core.node_base import update_node

TYPE_ITEMS = (
    ("CV_COMP_CORREL", "CV_COMP_CORREL", "CV_COMP_CORREL", "", 0)
    ("CV_COMP_CHISQR", "CV_COMP_CHISQR", "CV_COMP_CHISQR", "", 1)
    ("CV_COMP_CHISQR_ALT ", "CV_COMP_CHISQR_ALT ", "CV_COMP_CHISQR_ALT ", "", 2)
    ("CV_COMP_INTERSECT ", "CV_COMP_INTERSECT ", "CV_COMP_INTERSECT ", "", 3)
    ("CV_COMP_BHATTACHARYYA ", "CV_COMP_BHATTACHARYYA ", "CV_COMP_BHATTACHARYYA ", "", 4)
    ("CV_COMP_HELLINGER ", "CV_COMP_HELLINGER ", "CV_COMP_HELLINGER ", "", 5)
    ("CV_COMP_KL_DIV  ", "CV_COMP_KL_DIV  ", "CV_COMP_KL_DIV  ", "", 6)
)


class OCVLcompareHistNode(OCVLNodeBase):

    n_doc = "Compares two histograms."
    n_requirements = {}

    H1_in: bpy.props.StringProperty(name="H1_in", default=str(uuid.uuid4()), description="First compared histogram.")
    H2_in: bpy.props.StringProperty(name="H2_in", default=str(uuid.uuid4()), description="Second compared histogram of the same size as H1 .")
    method_in: bpy.props.EnumProperty(items=TYPE_ITEMS, default='CV_COMP_CORREL', update=update_node, description="Comparison method that could be one of the following.")

    retval_out: bpy.props.StringProperty(name="retval_out", default=str(uuid.uuid4()), description="Calculates the back projection of a histogram.")

    def init(self, context):
        self.inputs.new("ImageSocket", "H1_in")
        self.inputs.new("ImageSocket", "H2_in")

        self.outputs.new("StringsSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'H1_in': self.get_from_props("H1_in"),
            'H2_in': self.get_from_props("H2_in"),
        }

        retval_out = self.process_cv(fn=cv2.compareHist, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)

