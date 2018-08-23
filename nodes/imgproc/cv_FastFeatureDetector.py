import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


TYPE_FAST_ITEMS = (
    ("FastFeatureDetector_TYPE_5_8", "FastFeatureDetector_TYPE_5_8", "FastFeatureDetector_TYPE_5_8", "", 0),
    ("FastFeatureDetector_TYPE_7_12", "FastFeatureDetector_TYPE_7_12", "FastFeatureDetector_TYPE_7_12", "", 1),
    ("FastFeatureDetector_TYPE_9_16", "FastFeatureDetector_TYPE_9_16", "FastFeatureDetector_TYPE_9_16", "", 2),
    ("FastFeatureDetector_THRESHOLD", "FastFeatureDetector_THRESHOLD", "FastFeatureDetector_THRESHOLD", "", 3),
    ("FastFeatureDetector_NONMAX_SUPPRESSION", "FastFeatureDetector_NONMAX_SUPPRESSION", "FastFeatureDetector_NONMAX_SUPPRESSION", "", 4),
    ("FastFeatureDetector_FAST_N", "FastFeatureDetector_FAST_N", "FastFeatureDetector_FAST_N", "", 5),
)


class OCVLFastFeatureDetectorNode(OCVLNode):

    _doc = _("Wrapping class for feature detection using the FAST method.")
    _url = "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_fast/py_fast.html"

    image_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Input 8-bit or floating-point 32-bit, single-channel image."))
    mask_in = StringProperty(default=str(uuid.uuid4()), update=updateNode,
        description=_("Optional region of interest."))

    threshold_in = IntProperty(default=10, min=1, max=100, update=updateNode,
        description=_(""))
    type_in = EnumProperty(items=TYPE_FAST_ITEMS, default="FastFeatureDetector_TYPE_9_16", update=updateNode,
        description=_(""))
    nonmaxSuppression_in = BoolProperty(default=False, update=updateNode,
        description=_(""))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "mask_in")
        self.inputs.new("StringsSocket", "threshold_in").prop_name = "threshold_in"

        self.outputs.new("StringsSocket", "keypoints_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs_init = self.clean_kwargs({
            'threshold_in': self.get_from_props("threshold_in"),
            'type_in': self.get_from_props("type_in"),
            'nonmaxSuppression_in': self.get_from_props("nonmaxSuppression_in"),
            })

        kwargs_detect = self.clean_kwargs({
            'image': self.get_from_props("image_in"),
            'mask': None  # self.get_from_props("mask_in"),
        })

        fast = cv2.FastFeatureDetector_create(**kwargs_init)
        keypoints_out = self.process_cv(fn=fast.detect, kwargs=kwargs_detect)
        self.refresh_output_socket("keypoints_out", keypoints_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, prop_name='type_in')


def register():
    cv_register_class(OCVLFastFeatureDetectorNode)


def unregister():
    cv_unregister_class(OCVLFastFeatureDetectorNode)
