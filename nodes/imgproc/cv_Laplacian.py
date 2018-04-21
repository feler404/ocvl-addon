import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntProperty, FloatProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, COLOR_DEPTH_ITEMS, BORDER_TYPE_ITEMS


class OCVLLaplacianNode(OCVLNode):

    _doc = _("Calculates the Laplacian of an image.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))

    def set_ksize(self, value):
        if value % 2 == 0:
            value = value + 1
        self["ksize_in"] = value

    def get_ksize(self):
        return self.get("ksize_in", 1)

    ddepth_in = EnumProperty(items=COLOR_DEPTH_ITEMS, default='CV_8U', update=updateNode,
        description=_("Desired depth of the destination image."))
    ksize_in = IntProperty(default=1, update=updateNode, min=1, max=10, set=set_ksize, get=get_ksize,
        description=_("Aperture size used to compute the second-derivative filters."))
    scale_in = FloatProperty(default=1.0, min=1, max=8, update=updateNode,
        description=_("Optional scale factor for the computed Laplacian values."))
    delta_in = FloatProperty(default=0.0, min=0, max=255, update=updateNode,
        description=_("Optional delta value that is added to the results prior to storing them in dst."))
    borderType_in = EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=updateNode,
        description=_("Pixel extrapolation method, see cv::BorderTypes."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('StringsSocket', "scale_in").prop_name = 'scale_in'
        self.inputs.new('StringsSocket', "delta_in").prop_name = 'delta_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'src': self.get_from_props("image_in"),
            'ddepth_in': self.get_from_props("ddepth_in"),
            'ksize_in': int(self.get_from_props("ksize_in")),
            'scale_in': self.get_from_props("scale_in"),
            'delta_in': self.get_from_props("delta_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        image_out = self.process_cv(fn=cv2.Laplacian, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')
        self.add_button(layout, 'ddepth_in')


def register():
    cv_register_class(OCVLLaplacianNode)


def unregister():
    cv_unregister_class(OCVLLaplacianNode)
