import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatVectorProperty, IntVectorProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, LINE_TYPE_ITEMS, updateNode


class OCVLdrawContoursNode(OCVLNode):

    _doc=_("Draws contours outlines or filled contours.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()), description=_("Input image."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()), description=_("Output image."))

    contours = StringProperty(default="", update=updateNode,
        description=_("All the input contours. Each contour is stored as a point vector."))
    contourIdx = IntProperty(default=-1, min=-1, max=10, update=updateNode,
        description=_("Parameter indicating a contour to draw. If it is negative, all the contours are drawn."))
    color = FloatVectorProperty(update=updateNode, default=(.7, .7, .1, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR',
        description=_("Color of the contours."))
    thickness = IntProperty(default=2, min=1, max=10, update=updateNode,
        description=_("Thickness of lines the contours are drawn with. If it is negative (for example, thickness=CV_FILLED ), the contour interiors are drawn."))
    lineType = EnumProperty(items=LINE_TYPE_ITEMS, default="LINE_AA",update=updateNode,
        description=_("Line connectivity. See cv::LineTypes."))
    hierarchy = StringProperty(default="", update=updateNode,
        description=_("Optional information about hierarchy. It is only needed if you want to draw only some of the contours (see maxLevel )."))
    maxLevel = IntProperty(default=1, min=0, max=10, update=updateNode,
        description=_("""Maximal level for drawn contours. If it is 0, only the specified contour is drawn.
        .   If it is 1, the function draws the contour(s) and all the nested contours. If it is 2, the function
        .   draws the contours, all the nested contours, all the nested-to-nested contours, and so on. This
        .   parameter is only taken into account when there is hierarchy available."""))
    offset = IntVectorProperty(default=(0, 0), size=2, update=updateNode,
        description=_("Optional contour shift parameter. Shift all the drawn contours by the specified \f$\texttt{offset}=(dx,dy)\f$ ."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "contours")
        self.inputs.new('StringsSocket', "hierarchy")
        self.inputs.new('StringsSocket', "contourIdx").prop_name = 'contourIdx'
        self.inputs.new('SvColorSocket', 'color').prop_name = 'color'
        self.inputs.new('StringsSocket', "thickness").prop_name = 'thickness'
        self.inputs.new('StringsSocket', "maxLevel").prop_name = 'maxLevel'
        self.inputs.new('StringsSocket', "offset").prop_name = 'offset'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'image': self.get_from_props("image_in"),
            'contours': self.get_from_props("contours"),
            'hierarchy': self.get_from_props("hierarchy"),
            'contourIdx': self.get_from_props("contourIdx"),
            'color': self.get_from_props("color"),
            'thickness': self.get_from_props("thickness"),
            'lineType': self.get_from_props("lineType"),
            'maxLevel': self.get_from_props("maxLevel"),
            'offset': self.get_from_props("offset"),
            }

        image_out = self.process_cv(fn=cv2.drawContours, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'lineType')


def register():
    cv_register_class(OCVLdrawContoursNode)


def unregister():
    cv_unregister_class(OCVLdrawContoursNode)
