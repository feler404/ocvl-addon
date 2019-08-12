import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


TYPE_ITEMS = (
    ("HISTCMP_CORREL", "HISTCMP_CORREL", "HISTCMP_CORREL", "", 0),
    ("HISTCMP_CHISQR", "HISTCMP_CHISQR", "HISTCMP_CHISQR", "", 1),
    ("HISTCMP_CHISQR_ALT", "HISTCMP_CHISQR_ALT", "HISTCMP_CHISQR_ALT", "", 2),
    ("HISTCMP_INTERSECT", "HISTCMP_INTERSECT", "HISTCMP_INTERSECT", "", 3),
    ("HISTCMP_BHATTACHARYYA", "HISTCMP_BHATTACHARYYA", "HISTCMP_BHATTACHARYYA", "", 4),
    ("HISTCMP_HELLINGER", "HISTCMP_HELLINGER", "HISTCMP_HELLINGER", "", 5),
    ("HISTCMP_KL_DIV", "HISTCMP_KL_DIV", "HISTCMP_KL_DIV", "", 6),
)


class OCVLcompareHistNode(OCVLNodeBase):

    n_doc = "Compares two histograms."
    n_requirements = {}

    H1_in: bpy.props.StringProperty(name="H1_in", default=str(uuid.uuid4()), description="First compared histogram.")
    H2_in: bpy.props.StringProperty(name="H2_in", default=str(uuid.uuid4()), description="Second compared histogram of the same size as H1 .")
    method_in: bpy.props.EnumProperty(items=TYPE_ITEMS, default='HISTCMP_CORREL', update=update_node, description="Comparison method that could be one of the following.")

    retval_out: bpy.props.StringProperty(name="retval_out", default=str(uuid.uuid4()), description="Calculates the back projection of a histogram.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "H1_in")
        self.inputs.new("OCVLImageSocket", "H2_in")

        self.outputs.new("OCVLObjectSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'H1_in': self.get_from_props("H1_in"),
            'H2_in': self.get_from_props("H2_in"),
            'method_in': self.get_from_props("method_in"),
        }

        retval_out = self.process_cv(fn=cv2.compareHist, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "method_in")
