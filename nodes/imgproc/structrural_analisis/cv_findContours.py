import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, RETRIEVAL_MODE_ITEMS, APPROXIMATION_MODE_ITEMS


class OCVLfindContoursNode(OCVLNodeBase):

    n_doc = "Finds contours in a binary image."
    n_quick_link_requirements = {"image_in": {"code_in": "COLOR_BGR2GRAY", "color_in": (0, 0, 0, 0)}}
    n_requirements = {"__and__": ["image_in"]}

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()), description="Input image.")
    mode_in: bpy.props.EnumProperty(items=RETRIEVAL_MODE_ITEMS, default="RETR_TREE", update=update_node, description="Contour retrieval mode, see cv::RetrievalModes")
    method_in: bpy.props.EnumProperty(items=APPROXIMATION_MODE_ITEMS, default="CHAIN_APPROX_SIMPLE", update=update_node, description="Contour approximation method, see cv::ContourApproximationModes")
    offset_in: bpy.props.IntVectorProperty(default=(0, 0), size=2, update=update_node, description="Optional offset by which every contour point is shifted. This is useful if the.")

    image_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()), description="Output image.")
    contours_out: bpy.props.StringProperty(name="contours_out", default=str(uuid.uuid4()), description="Detected contours. Each contour is stored as a vector of points.")
    hierarchy_out: bpy.props.StringProperty(name="hierarchy_out", default=str(uuid.uuid4()), description="Optional output vector, containing information about the image topology. It has as many elements as the number of contours.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "image_in")
        self.inputs.new('OCVLObjectSocket', "offset_in").prop_name = 'offset_in'

        self.outputs.new("OCVLImageSocket", "image_out")
        self.outputs.new("OCVLContourSocket", "contours_out")
        self.outputs.new("OCVLObjectSocket", "hierarchy_out")

    def wrapped_process(self):
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
