import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from .abc_Feature2D import OCVLFeature2DNode, WORK_MODE_ITEMS, STATE_MODE_ITEMS
from ...operatores.abc import InitFeature2DOperator
from ...globals import FEATURE2D_INSTANCES_DICT
from ...utils import cv_register_class, cv_unregister_class, updateNode


MSER_WORK_MODE_ITEMS = (
    ("DETECT", "DETECT", "DETECT", "", 0),
    ("COMPUTE", "COMPUTE", "COMPUTE", "CANCEL", 1),
    ("DETECT-COMPUTE", "DETECT-COMPUTE", "DETECT-COMPUTE", "CANCEL", 2),
)


class OCVLMSERNode(OCVLFeature2DNode):

    _doc = _("Maximally stable extremal region extractor.")
    _init_method = cv2.MSER_create

    def update_layout(self, context):
        self.update_sockets(context)
        updateNode(self, context)

    def update_and_init(self, context):
        InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_layout()

    image_in = StringProperty(default=str(uuid.uuid4()), description=_("Input 8-bit or floating-point 32-bit, single-channel image."))
    mask_in = StringProperty(default=str(uuid.uuid4()), description=_("Optional region of interest."))
    keypoints_in = StringProperty(default=str(uuid.uuid4()), description=_(""))

    keypoints_out = StringProperty(default=str(uuid.uuid4()), description=_(""))
    descriptors_out = StringProperty(default=str(uuid.uuid4()), description=_(""))

    loc_file_load = StringProperty(default="/", description=_(""))
    loc_file_save = StringProperty(default="/", description=_(""))
    loc_work_mode = EnumProperty(items=MSER_WORK_MODE_ITEMS, default="DETECT", update=update_layout, description=_(""))
    loc_state_mode = EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description=_(""))
    loc_descriptor_size = IntProperty(default=0, description=_(""))
    loc_descriptor_type = IntProperty(default=0, description=_(""))
    loc_default_norm = IntProperty(default=0, description=_(""))
    loc_class_repr = StringProperty(default="", description=_(""))

    T1_delta_init = IntProperty(default=5, min=1, max=100, update=update_and_init, description="")
    T1_min_area_init = IntProperty(default=30, min=1, max=100000, update=update_and_init, description="")
    T1_max_area_init = IntProperty(default=14400, min=1, max=1000000, update=update_and_init, description="")
    T1_max_variation_init = FloatProperty(default=0.25, min=0.0001, max=0.9999, update=update_and_init, description="")
    T1_min_diversity_init = FloatProperty(default=0.2, min=0.0001, max=0.9999, update=update_and_init, description="")
    T1_max_evolution_init = IntProperty(default=200, min=1, max=1000, update=update_and_init, description="")
    T1_area_threshold_init = FloatProperty(default=1.01, min=1000.0, update=update_and_init, description="")
    T1_min_margin_init = FloatProperty(default=0.003, min=0.0001, max=0.9999, update=update_and_init, description="")
    T1_edge_blur_size_init = IntProperty(default=5, min=1, max=1000, update=update_and_init, description="")

    def sv_init(self, context):
        super().sv_init(context)

    def wrapped_process(self):
        instance = FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

        if self.loc_work_mode == "DETECT":
            self._detect(instance)
        elif self.loc_work_mode == "COMPUTE":
            self._compute(instance)
        elif self.loc_work_mode == "DETECT-COMPUTE":
            self._detect_and_compute(instance)


def register():
    cv_register_class(OCVLMSERNode)


def unregister():
    cv_unregister_class(OCVLMSERNode)
