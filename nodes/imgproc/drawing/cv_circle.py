import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, LINE_TYPE_ITEMS


class OCVLcircleNode(OCVLNodeBase):

    bl_icon = 'GREASEPENCIL'

    n_doc = "Draws a circle."
    n_quick_link_requirements = {"img_in": {"loc_image_mode": "PLANE"}}
    n_requirements = {"__and__": ["img_in"]}

    img_in: bpy.props.StringProperty(name="img_in", default=str(uuid.uuid4()), description="Input image.")
    img_out: bpy.props.StringProperty(name="img_out", default=str(uuid.uuid4()), description="Output image.")

    center_in: bpy.props.IntVectorProperty(default=(40, 40), size=2, update=update_node, description="Center of the circle.")
    radius_in: bpy.props.IntProperty(default=30, min=1, max=100, update=update_node, description="Radius of the circle.")
    color_in: bpy.props.FloatVectorProperty(update=update_node, default=(.7, .7, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR', description="Circle color.")
    thickness_in: bpy.props.IntProperty(default=2, min=-1, max=10, update=update_node, description="Thickness of the circle outline, if positive. Negative thickness means that a filled circle is to be drawn.")
    lineType_in: bpy.props.EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA",update=update_node, description="Type of the circle boundary. See the line description.")
    shift_in: bpy.props.IntProperty(default=0, min=0, max=10, update=update_node, description="Number of fractional bits in the coordinates of the center and in the radius value.")

    def init(self, context):
        self.width = 260
        self.inputs.new("OCVLImageSocket", "img_in")
        self.inputs.new('OCVLObjectSocket', "center_in").prop_name = 'center_in'
        self.inputs.new('OCVLObjectSocket', "radius_in").prop_name = 'radius_in'
        self.inputs.new('OCVLColorSocket', 'color_in').prop_name = 'color_in'
        self.inputs.new('OCVLObjectSocket', "thickness_in").prop_name = 'thickness_in'
        self.inputs.new('OCVLObjectSocket', "shift_in").prop_name = 'shift_in'

        self.outputs.new("OCVLImageSocket", "img_out")

    def wrapped_process(self):
        kwargs = {
            'img_in': self.get_from_props("img_in"),
            'center_in': self.get_from_props("center_in"),
            'color_in': self.get_from_props("color_in"),
            'thickness_in': self.get_from_props("thickness_in"),
            'radius_in': self.get_from_props("radius_in"),
            'lineType_in': self.get_from_props("lineType_in"),
            'shift_in': self.get_from_props("shift_in"),
            }

        img_out = self.process_cv(fn=cv2.circle, kwargs=kwargs)
        self.refresh_output_socket("img_out", img_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'lineType_in')
