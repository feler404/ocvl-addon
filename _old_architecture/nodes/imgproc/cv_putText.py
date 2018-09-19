import cv2
import uuid

import bpy

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLputTextNode(OCVLNodeBase):
    bl_icon = 'GREASEPENCIL'

    n_doc = "Draws a text string."

    image_in = bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()),
        description="Input image.")
    image_out = bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()),
        description="Output image.")

    text = bpy.props.StringProperty(default="OpenCV", update=update_node,
        description="Text string to be drawn.")
    org = bpy.props.IntVectorProperty(default=(0, 0), size=2, update=update_node,
        description="Bottom-left corner of the text string in the image.")
    fontScale = bpy.props.IntProperty(default=5, min=1, max=30,update=update_node,
        description="Scale factor that is multiplied by the font-specific base size.")
    fontFace = bpy.props.EnumProperty(items=FONT_FACE_ITEMS, default="FONT_HERSHEY_SIMPLEX", update=update_node,
        description="Font type, see cv::HersheyFonts.")
    color = bpy.props.FloatVectorProperty(update=update_node, default=(.9, .9, .2, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR',
        description="Text color.")
    thickness = bpy.props.IntProperty(default=2, min=1, max=10, update=update_node,
        description="Thickness of the lines used to draw a text.")
    lineType = bpy.props.EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA",update=update_node,
        description="Line type. See the line for details.")
    bottomLeftOrigin = bpy.props.BoolProperty(default=False, update=update_node,
        description="When true, the image data origin is at the bottom-left corner. Otherwise, it is at the top-left corner.")

    def init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "text").prop_name = 'text'
        self.inputs.new('StringsSocket', "org").prop_name = 'org'
        self.inputs.new('StringsSocket', "fontScale").prop_name = 'fontScale'
        self.inputs.new('StringsSocket', "thickness").prop_name = 'thickness'
        self.inputs.new('SvColorSocket', 'color').prop_name = 'color'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'img_in': self.get_from_props("image_in"),
            'text': self.get_from_props("text"),
            'org': self.get_from_props("org"),
            'fontFace': self.get_from_props("fontFace"),
            'fontScale': self.get_from_props("fontScale"),
            'color': self.get_from_props("color"),
            'thickness': self.get_from_props("thickness"),
            'lineType': self.get_from_props("lineType"),
            'bottomLeftOrigin': self.get_from_props("bottomLeftOrigin"),
            }

        image_out = self.process_cv(fn=cv2.putText, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "fontFace")
        self.add_button(layout, "lineType")
        self.add_button(layout, "bottomLeftOrigin")



