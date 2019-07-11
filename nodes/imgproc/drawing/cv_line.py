import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, LINE_TYPE_ITEMS


class OCVLlineNode(OCVLNodeBase):

    bl_icon = 'GREASEPENCIL'
    n_doc = "Draws a line segment connecting two points."
    n_requirements = {"__and__": ["img_in"]}
    n_quick_link_requirements = {"img_in": {"loc_image_mode": "PLANE"}}

    img_in: bpy.props.StringProperty(name="img_in", default=str(uuid.uuid4()), description="Input image")
    pt1_in: bpy.props.IntVectorProperty(default=(20, 20), size=2, update=update_node, description="First point of the line segment.")
    pt2_in: bpy.props.IntVectorProperty(default=(70, 30), size=2, update=update_node, description="Second point of the line segment.")
    color_in: bpy.props.FloatVectorProperty(update=update_node, default=(.7, .7, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR', description="Line color.")
    thickness_in: bpy.props.IntProperty(default=2, min=1, max=10, update=update_node, description="Line thickness.")
    lineType_in: bpy.props.EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA", update=update_node, description="Line type. See the line for details.")
    shift_in: bpy.props.IntProperty(default=0, min=1, max=100, update=update_node, description="Number of fractional bits in the point coordinates.")
    
    img_out: bpy.props.StringProperty(name="img_out", default=str(uuid.uuid4()), description="Output image")

    def init(self, context):
        self.width = 200
        self.inputs.new("ImageSocket", "img_in")
        self.inputs.new('StringsSocket', "pt1_in").prop_name = 'pt1_in'
        self.inputs.new('StringsSocket', "pt2_in").prop_name = 'pt2_in'
        self.inputs.new('StringsSocket', "thickness_in").prop_name = 'thickness_in'
        self.inputs.new('StringsSocket', "shift_in").prop_name = 'shift_in'
        self.inputs.new('ColorSocket', 'color_in').prop_name = 'color_in'

        self.outputs.new("ImageSocket", "img_out")

    def wrapped_process(self):
        kwargs = {
            'img_in': self.get_from_props("img_in"),
            'pt1_in': self.get_from_props("pt1_in"),
            'pt2_in': self.get_from_props("pt2_in"),
            'color_in': self.get_from_props("color_in"),
            'thickness_in': self.get_from_props("thickness_in"),
            'lineType_in': self.get_from_props("lineType_in"),
            }

        img_out = self.process_cv(fn=cv2.line, kwargs=kwargs)
        self.refresh_output_socket("img_out", img_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, prop_name='lineType_in')
        self.add_button_get_points(layout=layout, props_name=['pt1_in', 'pt2_in'])
