import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from .abc_Feature2D import OCVLFeature2DNode, WORK_MODE_ITEMS, STATE_MODE_ITEMS
from ...operatores.abc import InitFeature2DOperator
from ...globals import FEATURE2D_INSTANCES_DICT
from ...utils import cv_register_class, cv_unregister_class, updateNode


class OCVLSURFNode(OCVLFeature2DNode):

    _doc = _("Class for extracting Speeded Up Robust Features from an image.")
    _url = "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html"
    _init_method = cv2.xfeatures2d.SURF_create

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

    hessianThreshold_init = FloatProperty(default=100, min=10, max=1000, step=100, update=update_and_init, description=_("Threshold for hessian keypoint detector used in SURF."))
    nOctaves_init = IntProperty(default=4, min=1, max=10, update=update_and_init, description=_("Number of pyramid octaves the keypoint detector will use."))
    nOctaveLayers_init = IntProperty(default=3, min=1, max=3, update=update_and_init, description=_("Number of octave layers within each octave."))
    extended_init = BoolProperty(default=False, update=update_and_init, description=_("Extended descriptor flag (true - use extended 128-element descriptors; false - use 64-element descriptors)."))
    upright_init = BoolProperty(default=False, update=update_and_init, description=_("	Up-right or rotated features flag (true - do not compute orientation of features; false - compute orientation)."))

    def sv_init(self, context):
        super().sv_init(context)

    def wrapped_process(self):
        surf = FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

        if self.loc_work_mode == "DETECT":
            self._detect(surf)
        elif self.loc_work_mode == "COMPUTE":
            self._compute(surf)
        elif self.loc_work_mode == "DETECT-COMPUTE":
            self._detect_and_compute(surf)


def register():
    cv_register_class(OCVLSURFNode)


def unregister():
    cv_unregister_class(OCVLSURFNode)
