import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, BORDER_TYPE_REQUIRED_ITEMS


class OCVLcopyMakeBorderNode(OCVLNodeBase):
    # bl_icon = 'BORDER_RECT'
    #
    n_doc = "Forms a border around an image."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image.")

    top_in: bpy.props.IntProperty(default=10, update=update_node, min=1, max=20, description="Border width in number of pixels in corresponding directions.")
    bottom_in: bpy.props.IntProperty(default=10, update=update_node, min=1, max=20, description="Border width in number of pixels in corresponding directions.")
    left_in: bpy.props.IntProperty(default=10, update=update_node, min=1, max=20, description="Border width in number of pixels in corresponding directions.")
    right_in: bpy.props.IntProperty(default=10, update=update_node, min=1, max=20, description="Border width in number of pixels in corresponding directions.")
    borderType_in: bpy.props.EnumProperty(items=BORDER_TYPE_REQUIRED_ITEMS, default='BORDER_DEFAULT', update=update_node, description="Border type. See borderInterpolate for details.")
    color_in: bpy.props.FloatVectorProperty(update=update_node, name='', default=(.3, .3, .2, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR', description="Border value if borderType==BORDER_CONSTANT.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new('OCVLObjectSocket', "top_in").prop_name = 'top_in'
        self.inputs.new('OCVLObjectSocket', "bottom_in").prop_name = 'bottom_in'
        self.inputs.new('OCVLObjectSocket', "left_in").prop_name = 'left_in'
        self.inputs.new('OCVLObjectSocket', "right_in").prop_name = 'right_in'
        self.inputs.new('OCVLColorSocket', "color_in").prop_name = "color_in"

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):

        kwargs = {
            'src': self.get_from_props("src_in"),
            'top_in': self.get_from_props("top_in"),
            'bottom_in': self.get_from_props("bottom_in"),
            'left_in': self.get_from_props("left_in"),
            'right_in': self.get_from_props("right_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            'value': self.get_from_props("color_in"),
            }

        dst_out = self.process_cv(fn=cv2.copyMakeBorder, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')
