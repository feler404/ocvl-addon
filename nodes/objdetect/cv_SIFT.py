import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from .cv_Feature2D import OCVLFeature2DNode, WORK_MODE_ITEMS, STATE_MODE_ITEMS
from ...operatores.feature2d_abc import InitFeature2DOperator
from ...globals import FEATURE2D_INSTANCES_DICT
from ...utils import cv_register_class, cv_unregister_class, updateNode


class OCVLSIFTNode(OCVLFeature2DNode):

    _doc = _("Class for extracting keypoints and computing descriptors using the Scale Invariant Feature Transform (SIFT) algorithm by D. Lowe")
    _url = "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.html"
    _init_method = cv2.xfeatures2d.SIFT_create

    def update_layout(self, context):
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

    nfeatures_init = IntProperty(default=0, min=0, max=100, update=updateNode,
        description=_("The number of best features to retain."))
    nOctaveLayers_init = IntProperty(default=3, min=1, max=3, update=updateNode,
        description=_("The number of layers in each octave."))
    contrastThreshold_init = FloatProperty(default=0.04, min=0.01, max=0.1, update=updateNode,
        description=_("The contrast threshold used to filter out weak features in semi-uniform (low-contrast) regions."))
    edgeThreshold_init = FloatProperty(default=10, min=0.1, max=100, update=updateNode,
        description=_("Size of an average block for computing a derivative covariation matrix over each pixel neighborhood."))
    sigma_init = FloatProperty(default=1.6, min=0.1, max=5., update=updateNode,
        description="The sigma of the Gaussian applied to the input image at the octave #0.")

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
    cv_register_class(OCVLSIFTNode)


def unregister():
    cv_unregister_class(OCVLSIFTNode)
