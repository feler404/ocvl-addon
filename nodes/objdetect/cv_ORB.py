import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from .abc_Feature2D import OCVLFeature2DNode, WORK_MODE_ITEMS, STATE_MODE_ITEMS
from ...operatores.abc import InitFeature2DOperator
from ...globals import FEATURE2D_INSTANCES_DICT
from ...utils import cv_register_class, cv_unregister_class, updateNode


SCORE_TYPE_ITEMS = (
    ("ORB_K_BYTES", "ORB_K_BYTES", "ORB_K_BYTES", "", 0),
    ("ORB_HARRIS_SCORE", "ORB_HARRIS_SCORE", "ORB_HARRIS_SCORE", "", 1),
    ("ORB_FAST_SCORE", "ORB_FAST_SCORE", "ORB_FAST_SCORE", "", 2),
)

class OCVLORBNode(OCVLFeature2DNode):

    _doc = _("Class implementing the ORB (oriented BRIEF) keypoint detector and descriptor extractor.")
    _url = "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_orb/py_orb.html"
    _init_method = cv2.ORB_create

    def update_layout(self, context):
        self.update_sockets(context)
        updateNode(self, context)

    def update_and_init(self, context):
        InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_sockets(context)
        updateNode(self, context)

    image_in = StringProperty(default=str(uuid.uuid4()), description=_("Input 8-bit or floating-point 32-bit, single-channel image."))
    mask_in = StringProperty(default=str(uuid.uuid4()), description=_("Optional region of interest."))
    keypoints_in = StringProperty(default=str(uuid.uuid4()), description=_(""))

    keypoints_out = StringProperty(default=str(uuid.uuid4()), description=_(""))
    descriptors_out = StringProperty(default=str(uuid.uuid4()), description=_(""))

    loc_file_load = StringProperty(default="/", description=_(""))
    loc_file_save = StringProperty(default="/", description=_(""))
    loc_work_mode = EnumProperty(items=WORK_MODE_ITEMS, default="DETECT-COMPUTE", update=update_layout, description=_(""))
    loc_state_mode = EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description=_(""))
    loc_descriptor_size = IntProperty(default=0, description=_(""))
    loc_descriptor_type = IntProperty(default=0, description=_(""))
    loc_default_norm = IntProperty(default=0, description=_(""))
    loc_class_repr = StringProperty(default="", description=_(""))

    scoreType_init = EnumProperty(default="ORB_HARRIS_SCORE", items=SCORE_TYPE_ITEMS, update=update_and_init,
        description=_("The default HARRIS_SCORE means that Harris algorithm is used to rank features."))
    nfeatures_init = IntProperty(default=500, min=1, max=10000, update=update_and_init,
        description=_("The maximum number of features to retain."))
    scaleFactor_init = FloatProperty(default=1.2, min=1.1, max=10., update=update_and_init,
        description=_("Pyramid decimation ratio, greater than 1. scaleFactor==2 means the classical pyramid."))
    nlevels_init = IntProperty(default=8, min=2, max=16, update=update_and_init,
        description=_("The number of pyramid levels."))
    edgeThreshold_init = IntProperty(default=31, min=10, max=100, update=update_and_init,
        description=_("This is size of the border where the features are not detected."))
    firstLevel_init = IntProperty(default=0, min=0, max=0, update=update_and_init,
        description=_("It should be 0 in the current implementation."))
    WTA_K_init = IntProperty(default=2, min=0, max=4, update=update_and_init,
        description=_("The number of points that produce each element of the oriented BRIEF descriptor."))
    patchSize_init = IntProperty(default=31, min=1, max=100, update=update_and_init,
        description=_("Size of the patch used by the oriented BRIEF descriptor."))
    fastThreshold_init = IntProperty(default=20, min=1, max=100, update=update_and_init,
        description=_("fastThreshold_in"))

    def sv_init(self, context):
        super().sv_init(context)

    def wrapped_process(self):
        sift = FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

        if self.loc_work_mode == "DETECT":
            self._detect(sift)
        elif self.loc_work_mode == "COMPUTE":
            self._compute(sift)
        elif self.loc_work_mode == "DETECT-COMPUTE":
            self._detect_and_compute(sift)


def register():
    cv_register_class(OCVLORBNode)


def unregister():
    cv_unregister_class(OCVLORBNode)
