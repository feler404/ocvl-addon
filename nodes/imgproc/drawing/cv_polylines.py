import uuid

import bpy
import cv2
import numpy as np
from ocvl.core.node_base import OCVLNodeBase, update_node, LINE_TYPE_ITEMS


class OCVLpolylinesNode(OCVLNodeBase):

    bl_icon = 'GREASEPENCIL'
    n_doc = "Draws several polygonal curves."
    n_requirements = {"__and__": ["img_in", "pts_in"]}
    n_quick_link_requirements = {
        "img_in": {"loc_image_mode": "PLANE"},
        "pts_in": {"__type_node__": "OCVLMatNode", "loc_input_mode": "MANUAL", "value_type_in": "float32", "loc_manual_input": "[[10, 10], [20, 80], [70, 90]]"},
    }


    img_in: bpy.props.StringProperty(name="img_in", default=str(uuid.uuid4()), description="Input image.")
    pts_in: bpy.props.StringProperty(default=str(uuid.uuid4()), update=update_node, description="Array of polygonal curves.")
    isClosed_in: bpy.props.BoolProperty(default=False, update=update_node, description="Flag indicating whether the drawn polylines are closed or not. If they are closed, the function draws a line from the last vertex of each curve to its first vertex.")
    color_in: bpy.props.FloatVectorProperty(update=update_node, default=(.7, .7, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR', description="Polyline color.")
    thickness_in: bpy.props.IntProperty(default=2, min=1, max=10, update=update_node, description="Thickness of the polyline edges.")
    lineType_in: bpy.props.EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA", update=update_node, description="Type of the line segments. See the line description.")
    shift_in: bpy.props.IntProperty(default=0, min=0, max=100, update=update_node, description="Number of fractional bits in the vertex coordinates.")

    img_out: bpy.props.StringProperty(name="img_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.width = 150
        self.inputs.new("ImageSocket", "img_in")
        self.inputs.new('ImageSocket', "pts_in")
        self.inputs.new('StringsSocket', "thickness_in").prop_name = 'thickness_in'
        self.inputs.new('StringsSocket', "shift_in").prop_name = 'shift_in'
        self.inputs.new('ColorSocket', 'color_in').prop_name = 'color_in'

        self.outputs.new("ImageSocket", "img_out")

    def wrapped_process(self):
        kwargs = {
            'img_in': self.get_from_props("img_in"),
            'pts_in': np.int32([self.get_from_props("pts_in")]),
            'isClosed_in': self.get_from_props("isClosed_in"),
            'color_in': self.get_from_props("color_in"),
            'thickness_in': self.get_from_props("thickness_in"),
            'lineType_in': self.get_from_props("lineType_in"),
            'shift_in': self.get_from_props("shift_in"),
            }

        img_out = self.process_cv(fn=cv2.polylines, kwargs=kwargs)
        self.refresh_output_socket("img_out", img_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'lineType_in')
        self.add_button(layout, 'isClosed_in')
