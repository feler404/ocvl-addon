import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatVectorProperty, IntVectorProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, LINE_TYPE_ITEMS


class OCVLarrowedLineNode(OCVLNode):

    bl_icon = 'GREASEPENCIL'

    _doc = _("Draws a arrow segment pointing from the first point to the second one.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    pt1_in = IntVectorProperty(default=(0, 0), size=2, update=updateNode,
        description=_("First point of the line segment."))
    pt2_in = IntVectorProperty(default=(1, 1), size=2, update=updateNode,
        description=_("Second point of the line segment."))
    color_in = FloatVectorProperty(update=updateNode, default=(.7, .7, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR',
        description=_("Line color."))
    thickness_in = IntProperty(default=2, min=1, max=10, update=updateNode,
        description=_("Line thickness."))
    lineType_in = EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA", update=updateNode,
        description=_("Line type."))
    shift_in = IntProperty(default=0, min=1, max=100, update=updateNode,
        description=_("Number of fractional bits in the point coordinates."))
    tipLength_in = FloatProperty(default=0.1, min=0, max=1.0, update=updateNode,
        description=_("The length of the arrow tip in relation to the arrow length."))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))

    def sv_init(self, context):
        self.width = 200
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "pt1_in").prop_name = 'pt1_in'
        self.inputs.new('StringsSocket', "pt2_in").prop_name = 'pt2_in'
        self.inputs.new('StringsSocket', "thickness_in").prop_name = 'thickness_in'
        self.inputs.new('StringsSocket', "shift_in").prop_name = 'shift_in'
        self.inputs.new('StringsSocket', 'tipLength_in').prop_name = 'tipLength_in'
        self.inputs.new('SvColorSocket', 'color_in').prop_name = 'color_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'img_in': self.get_from_props("image_in"),
            'pt1_in': self.get_from_props("pt1_in"),
            'pt2_in': self.get_from_props("pt2_in"),
            'color_in': self.get_from_props("color_in"),
            'thickness_in': self.get_from_props("thickness_in"),
            'line_type': self.get_from_props("lineType_in"),
            'tipLength_in': self.get_from_props("tipLength_in"),
            }

        image_out = self.process_cv(fn=cv2.arrowedLine, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, prop_name='lineType_in')
        self.add_button_get_points(layout=layout, props_name=['pt1_in', 'pt2_in'])


def register():
    cv_register_class(OCVLarrowedLineNode)


def unregister():
    cv_unregister_class(OCVLarrowedLineNode)
