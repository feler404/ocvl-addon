import cv2
import uuid
import numpy as np
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


SCORE_TYPE_ITEMS = (
    ("ORB_K_BYTES", "ORB_K_BYTES", "ORB_K_BYTES", "", 0),
    ("ORB_HARRIS_SCORE", "ORB_HARRIS_SCORE", "ORB_HARRIS_SCORE", "", 1),
    ("ORB_FAST_SCORE", "ORB_FAST_SCORE", "ORB_FAST_SCORE", "", 2),
)


class OCVLORBNode(OCVLNode):

    _doc = _("Class implementing the ORB (oriented BRIEF) keypoint detector and descriptor extractor.")
    _url = "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_orb/py_orb.html"

    image_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Input 8-bit or floating-point 32-bit, single-channel image."))
    mask_in = StringProperty(default=str(uuid.uuid4()), update=updateNode,
        description=_(""))

    scoreType_in = EnumProperty(default="ORB_HARRIS_SCORE", items=SCORE_TYPE_ITEMS, update=updateNode,
        description=_("The default HARRIS_SCORE means that Harris algorithm is used to rank features."))
    nfeatures_in = IntProperty(default=500, min=1, max=10000, update=updateNode,
        description=_("The maximum number of features to retain."))
    scaleFactor_in = FloatProperty(default=1.2, min=1.1, max=10., update=updateNode,
        description=_("Pyramid decimation ratio, greater than 1. scaleFactor==2 means the classical pyramid."))
    nlevels_in = IntProperty(default=8, min=2, max=16, update=updateNode,
        description=_("The number of pyramid levels."))
    edgeThreshold_in = IntProperty(default=31, min=10, max=100, update=updateNode,
        description=_("This is size of the border where the features are not detected."))
    firstLevel_in = IntProperty(default=0, min=0, max=0, update=updateNode,
        description=_("It should be 0 in the current implementation."))
    WTA_K_in = IntProperty(default=2, min=0, max=4, update=updateNode,
        description=_("The number of points that produce each element of the oriented BRIEF descriptor."))
    patchSize_in = IntProperty(default=31, min=1, max=100, update=updateNode,
        description=_("Size of the patch used by the oriented BRIEF descriptor."))
    fastThreshold_in = IntProperty(default=20, min=1, max=100, update=updateNode,
        description=_("fastThreshold_in"))

    keypoints_out = StringProperty(default=str(uuid.uuid4()),
        description=_("Output vector of detected keypoints."))
    descriptors_out = StringProperty(default=str(uuid.uuid4()),
        description=_("Output vector of detected descriptors."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "mask_in")
        self.inputs.new("StringsSocket", "scoreType_in")
        self.inputs.new("StringsSocket", "nfeatures_in").prop_name = "nfeatures_in"
        self.inputs.new("StringsSocket", "scaleFactor_in").prop_name = "scaleFactor_in"
        self.inputs.new("StringsSocket", "nlevels_in").prop_name = "nlevels_in"
        self.inputs.new("StringsSocket", "edgeThreshold_in").prop_name = "edgeThreshold_in"
        self.inputs.new("StringsSocket", "firstLevel_in").prop_name = "firstLevel_in"
        self.inputs.new("StringsSocket", "WTA_K_in").prop_name = "WTA_K_in"
        self.inputs.new("StringsSocket", "patchSize_in").prop_name = "patchSize_in"
        self.inputs.new("StringsSocket", "fastThreshold_in").prop_name = "fastThreshold_in"

        self.outputs.new("StringsSocket", "keypoints_out")
        self.outputs.new("StringsSocket", "descriptors_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs_init = self.clean_kwargs({
            'scoreType_in': int(self.get_from_props("scoreType_in")),
            'nfeatures_in': self.get_from_props("nfeatures_in"),
            'scaleFactor_in': self.get_from_props("scaleFactor_in"),
            'nlevels_in': self.get_from_props("nlevels_in"),
            'edgeThreshold_in': self.get_from_props("edgeThreshold_in"),
            'firstLevel_in': self.get_from_props("firstLevel_in"),
            'WTA_K_in': self.get_from_props("WTA_K_in"),
            'patchSize_in': self.get_from_props("patchSize_in"),
            'fastThreshold_in': self.get_from_props("fastThreshold_in"),
            })

        kwargs_detect = self.clean_kwargs({
            'image_in': self.get_from_props("image_in"),
            'mask_in': self.get_from_props("mask_in"),
        })

        if isinstance(kwargs_detect['mask'], str):
            kwargs_detect['mask'] = np.ones(kwargs_detect['image'].shape)

        orb = cv2.ORB_create(**kwargs_init)
        keypoints_out, descriptors_out = self.process_cv(fn=orb.detectAndCompute, kwargs=kwargs_detect)
        self.refresh_output_socket("keypoints_out", keypoints_out, is_uuid_type=True)
        self.refresh_output_socket("descriptors_out", descriptors_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, prop_name='scoreType_in')


def register():
    cv_register_class(OCVLORBNode)


def unregister():
    cv_unregister_class(OCVLORBNode)
