import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatVectorProperty, BoolProperty, IntVectorProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, FONT_FACE_ITEMS, LINE_TYPE_ITEMS, updateNode


class OCVLputTextNode(OCVLNode):
    bl_icon = 'GREASEPENCIL'

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    text = StringProperty(default="OpenCV", update=updateNode,
        description="Text string to be drawn.")
    org = IntVectorProperty(default=(0, 0), size=2, update=updateNode,
        description="Bottom-left corner of the text string in the image.")
    fontScale = IntProperty(default=5, min=1, max=30,update=updateNode,
        description="scale factor that is multiplied by the font-specific base size.")
    fontFace = EnumProperty(items=FONT_FACE_ITEMS, default="FONT_HERSHEY_SIMPLEX", update=updateNode,
        description="Font type, see cv::HersheyFonts.")
    color = FloatVectorProperty(update=updateNode, default=(.9, .9, .2, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR',
        description="Text color.")
    thickness = IntProperty(default=2, min=1, max=10, update=updateNode,
        description="Thickness of the lines used to draw a text.")
    lineType = EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA",update=updateNode,
        description="Line type. See the line for details.")
    bottomLeftOrigin = BoolProperty(default=False, update=updateNode,
        description="When true, the image data origin is at the bottom-left corner. Otherwise, it is at the top-left corner.")

    def sv_init(self, context):
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


def register():
    cv_register_class(OCVLputTextNode)


def unregister():
    cv_unregister_class(OCVLputTextNode)
