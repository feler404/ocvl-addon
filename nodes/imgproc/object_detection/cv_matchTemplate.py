import uuid

import bpy
import cv2
import numpy as np
from ocvl.core.node_base import OCVLNodeBase, update_node, TEMPLATE_MATCH_MODE_ITEMS


class OCVLmatchTemplateNode(OCVLNodeBase):

    n_doc = "Compares a template against overlapped image regions."
    n_requirements = {"__and__": ["image_in", "templ_in"]}
    n_quick_link_requirements = {"image_in": {"width_in": 100, "height_in": 100}, "templ_in": {"width_in": 96, "height_in": 88, "loc_image_mode": "PLANE"}}

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()), description="Image where the search is running. It must be 8-bit or 32-bit floating-point.")
    templ_in: bpy.props.StringProperty(name="templ_in", default=str(uuid.uuid4()), description="Searched template. It must be not greater than the source image and have the same data type.")
    method_in: bpy.props.EnumProperty(items=TEMPLATE_MATCH_MODE_ITEMS, default='TM_CCOEFF', update=update_node, description="Parameter specifying the comparison method, see cv::TemplateMatchModes.")
    loc_color_in: bpy.props.FloatVectorProperty(update=update_node, name='color_in', default=(.9, .1, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR')
    loc_threshold: bpy.props.FloatProperty(default=0.8, min=0, max=1, update=update_node, subtype="FACTOR")

    image_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()), description="Output image.")
    result_out: bpy.props.StringProperty(name="result_out", default=str(uuid.uuid4()), description="Map of comparison results. It must be single-channel 32-bit floating-point.")

    def init(self, context):
        self.width = 250
        self.inputs.new("OCVLImageSocket", "image_in")
        self.inputs.new('OCVLImageSocket', "templ_in")
        self.inputs.new('OCVLColorSocket', 'loc_color_in').prop_name = 'loc_color_in'
        self.inputs.new('OCVLObjectSocket', 'loc_threshold').prop_name = 'loc_threshold'

        self.outputs.new("OCVLImageSocket", "image_out")
        self.outputs.new("OCVLObjectSocket", "result_out")

    def wrapped_process(self):
        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'templ_in': self.get_from_props("templ_in"),
            'method_in': self.get_from_props("method_in"),
            }

        result_out = self.process_cv(fn=cv2.matchTemplate, kwargs=kwargs)
        image_out = np.copy(self.get_from_props("image_in"))
        h, w, *channels = self.get_from_props("templ_in").shape

        if not channels:
            image_out = cv2.cvtColor(image_out, cv2.COLOR_GRAY2RGB)
        elif channels[0] == 4:
            image_out = cv2.cvtColor(image_out, cv2.COLOR_RGBA2RGB)

        loc_color_in = self.get_from_props("loc_color_in")

        loc_threshold = self.get_from_props("loc_threshold")
        loc = np.where(result_out >= loc_threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(image_out, pt, (pt[0] + w, pt[1] + h), loc_color_in, 0)

        self.refresh_output_socket("result_out", result_out, is_uuid_type=True)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'method_in')
