import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, FONT_FACE_ITEMS, LINE_TYPE_ITEMS


class OCVLputTextNode(OCVLNodeBase):
    bl_icon = 'GREASEPENCIL'

    n_doc = "Draws a text string."
    n_requirements = {"__and__": ["img_in"]}
    n_quick_link_requirements = {"img_in": {"loc_image_mode": "PLANE"}}

    img_in: bpy.props.StringProperty(name="img_in", default=str(uuid.uuid4()), description="Input image.")
    text_in: bpy.props.StringProperty(default="Lab", update=update_node, description="Text string to be drawn.")
    org_in: bpy.props.IntVectorProperty(default=(0, 80), size=2, update=update_node, description="Bottom-left corner of the text string in the image.")
    fontScale_in: bpy.props.IntProperty(default=1, min=1, max=30,update=update_node, description="Scale factor that is multiplied by the font-specific base size.")
    fontFace_in: bpy.props.EnumProperty(items=FONT_FACE_ITEMS, default="FONT_HERSHEY_SIMPLEX", update=update_node, description="Font type, see cv::HersheyFonts.")
    color_in: bpy.props.FloatVectorProperty(update=update_node, default=(.9, .9, .2, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR', description="Text color.")
    thickness_in: bpy.props.IntProperty(default=2, min=1, max=10, update=update_node, description="Thickness of the lines used to draw a text.")
    lineType_in: bpy.props.EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA",update=update_node, description="Line type. See the line for details.")
    bottomLeftOrigin_in: bpy.props.BoolProperty(default=False, update=update_node, description="When true, the image data origin is at the bottom-left corner. Otherwise, it is at the top-left corner.")

    img_out: bpy.props.StringProperty(name="img_out", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.width = 250
        self.inputs.new("OCVLImageSocket", "img_in")
        self.inputs.new('OCVLObjectSocket', "text_in").prop_name = 'text_in'
        self.inputs.new('OCVLObjectSocket', "org_in").prop_name = 'org_in'
        self.inputs.new('OCVLObjectSocket', "fontScale_in").prop_name = 'fontScale_in'
        self.inputs.new('OCVLObjectSocket', "thickness_in").prop_name = 'thickness_in'
        self.inputs.new('OCVLColorSocket', 'color_in').prop_name = 'color_in'

        self.outputs.new("OCVLImageSocket", "img_out")

    def wrapped_process(self):
        kwargs = {
            'img_in': self.get_from_props("img_in"),
            'text_in': self.get_from_props("text_in"),
            'org_in': self.get_from_props("org_in"),
            'fontFace_in': self.get_from_props("fontFace_in"),
            'fontScale_in': self.get_from_props("fontScale_in"),
            'color_in': self.get_from_props("color_in"),
            'thickness_in': self.get_from_props("thickness_in"),
            'lineType_in': self.get_from_props("lineType_in"),
            'bottomLeftOrigin_in': self.get_from_props("bottomLeftOrigin_in"),
            }

        img_out = self.process_cv(fn=cv2.putText, kwargs=kwargs)
        self.refresh_output_socket("img_out", img_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "fontFace_in")
        self.add_button(layout, "lineType_in")
        self.add_button(layout, "bottomLeftOrigin_in")
