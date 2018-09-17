import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from .abc_Feature2D import OCVLFeature2DNode, WORK_MODE_ITEMS, STATE_MODE_ITEMS
from ...operatores.abc import InitFeature2DOperator
from ...globals import FEATURE2D_INSTANCES_DICT
from ...utils import cv_register_class, cv_unregister_class, updateNode


BYTES_ITEMS = (
    ("16", "16", "16", "", 0),
    ("32", "32", "32", "", 1),
    ("64", "64", "64", "", 2),
)

BDE_WORK_MODE_ITEMS = (
    ("DETECT", "DETECT", "DETECT", "CANCEL", 0),
    ("COMPUTE", "COMPUTE", "COMPUTE", "", 1),
    ("DETECT-COMPUTE", "DETECT-COMPUTE", "DETECT-COMPUTE", "CANCEL", 2),
)

class OCVLBriefDescriptorExtractorNode(OCVLFeature2DNode):

    _doc = _("Class for computing BRIEF descriptors described in [27].")
    _url = "https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_brief/py_brief.html#brief"
    _init_method = cv2.xfeatures2d.BriefDescriptorExtractor_create

    def update_layout(self, context):
        self.update_sockets(context)
        updateNode(self, context)

    def update_and_init(self, context):
        InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_layout(context)

    image_in = StringProperty(default=str(uuid.uuid4()), description=_("Input 8-bit or floating-point 32-bit, single-channel image."))
    mask_in = StringProperty(default=str(uuid.uuid4()), description=_("Optional region of interest."))
    keypoints_in = StringProperty(default=str(uuid.uuid4()), description=_(""))

    keypoints_out = StringProperty(default=str(uuid.uuid4()), description=_(""))
    descriptors_out = StringProperty(default=str(uuid.uuid4()), description=_(""))

    loc_file_load = StringProperty(default="/", description=_(""))
    loc_file_save = StringProperty(default="/", description=_(""))
    loc_work_mode = EnumProperty(items=BDE_WORK_MODE_ITEMS, default="COMPUTE", update=update_layout, description=_(""))
    loc_state_mode = EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description=_(""))
    loc_descriptor_size = IntProperty(default=0, description=_(""))
    loc_descriptor_type = IntProperty(default=0, description=_(""))
    loc_default_norm = IntProperty(default=0, description=_(""))
    loc_class_repr = StringProperty(default="", description=_(""))

    bytes_init = EnumProperty(items=BYTES_ITEMS, default="32", update=update_and_init, description=_(""))
    use_orientation_init = BoolProperty(default=False, update=update_and_init, description=_(""))

    def sv_init(self, context):
        super().sv_init(context)

    def wrapped_process(self):
        sift = FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

        if self.loc_work_mode == "DETECT":
            # self._detect(sift)
            pass
        elif self.loc_work_mode == "COMPUTE":
            self._compute(sift)
            # pass
        elif self.loc_work_mode == "DETECT-COMPUTE":
            #self._detect_and_compute(sift)
            pass


def register():
    cv_register_class(OCVLBriefDescriptorExtractorNode)


def unregister():
    cv_unregister_class(OCVLBriefDescriptorExtractorNode)
