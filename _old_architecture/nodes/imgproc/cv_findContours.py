import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, RETRIEVAL_MODE_ITEMS, APPROXIMATION_MODE_ITEMS, updateNode


class OCVLfindContoursNode(OCVLNode):

    _doc = _("Finds contours in a binary image.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))
    contours_out = StringProperty(name="contours_out", default=str(uuid.uuid4()),
        description=_("Detected contours. Each contour is stored as a vector of points."))
    hierarchy_out = StringProperty(name="hierarchy_out", default=str(uuid.uuid4()),
        description=_("Optional output vector, containing information about the image topology. It has as many elements as the number of contours."))

    mode_in = EnumProperty(items=RETRIEVAL_MODE_ITEMS, default="RETR_TREE", update=updateNode,
        description=_("Contour retrieval mode, see cv::RetrievalModes"))
    method_in = EnumProperty(items=APPROXIMATION_MODE_ITEMS, default="CHAIN_APPROX_SIMPLE", update=updateNode,
        description=_("Contour approximation method, see cv::ContourApproximationModes"))
    offset_in = IntVectorProperty(default=(0, 0), size=2, update=updateNode,
        description=_("Optional offset by which every contour point is shifted. This is useful if the."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "offset_in").prop_name = 'offset_in'

        self.outputs.new("StringsSocket", "image_out")
        self.outputs.new("StringsSocket", "contours_out")
        self.outputs.new("StringsSocket", "hierarchy_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'mode_in': self.get_from_props("mode_in"),
            'method_in': self.get_from_props("method_in"),
            'offset_in': self.get_from_props("offset_in"),
            }

        image_out, contours_out, hierarchy_out = self.process_cv(fn=cv2.findContours, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)
        self.refresh_output_socket("contours_out", contours_out, is_uuid_type=True)
        self.refresh_output_socket("hierarchy_out", hierarchy_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'mode_in')
        self.add_button(layout, 'method_in')


def register():
    cv_register_class(OCVLfindContoursNode)


def unregister():
    cv_unregister_class(OCVLfindContoursNode)
