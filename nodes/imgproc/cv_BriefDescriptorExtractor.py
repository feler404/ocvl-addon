import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


BYTES_ITEMS = (
    ("16", "16", "16", "", 0),
    ("32", "32", "32", "", 1),
    ("64", "64", "64", "", 2),
)


class OCVLBriefDescriptorExtractorNode(OCVLNode):

    _doc = _("Wrapping class for feature detection using the FAST method.")
    _url = "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_fast/py_fast.html"

    image_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Input 8-bit or floating-point 32-bit, single-channel image."))
    keypoints_in = StringProperty(default=str(uuid.uuid4()), update=updateNode,
        description=_(""))

    bytes_in = EnumProperty(items=BYTES_ITEMS, default="32", update=updateNode,
        description=_("Legth of the descriptor in bytes, valid values are: 16, 32 (default) or 64."))
    use_orientation_in = BoolProperty(default=False, update=updateNode,
        description=_("Sample patterns using keypoints orientation, disabled by default."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "keypoints_in")
        self.inputs.new("StringsSocket", "use_orientation_in").prop_name = "use_orientation_in"

        self.outputs.new("StringsSocket", "keypoints_out")
        self.outputs.new("StringsSocket", "descriptors_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in", "keypoints_in"])

        kwargs_init = self.clean_kwargs({
            'bytes_in': int(self.get_from_props("bytes_in")),
            'use_orientation_in': self.get_from_props("use_orientation_in"),
            })

        args_detect = self.get_from_props("image_in"), self.get_from_props("keypoints_in")  #

        brief = cv2.xfeatures2d.BriefDescriptorExtractor_create(**kwargs_init)
        keypoints_out, descriptors_out = brief.compute(*args_detect)
        self.refresh_output_socket("keypoints_out", keypoints_out, is_uuid_type=True)
        self.refresh_output_socket("descriptors_out", descriptors_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, prop_name='bytes_in')


def register():
    cv_register_class(OCVLBriefDescriptorExtractorNode)


def unregister():
    cv_unregister_class(OCVLBriefDescriptorExtractorNode)
