import cv2
import uuid

import bpy

from .abc_Feature2D import OCVLFeature2DNode, WORK_MODE_ITEMS, STATE_MODE_ITEMS
from ...operatores.abc import InitFeature2DOperator
from ...globals import FEATURE2D_INSTANCES_DICT
from ocvl.core.node_base import OCVLNodeBase, update_node


TYPE_ITEMS = (
    ("AGAST_FEATURE_DETECTOR_AGAST_5_8", "AGAST_FEATURE_DETECTOR_AGAST_5_8", "AGAST_FEATURE_DETECTOR_AGAST_5_8", "", 0),
    ("AGAST_FEATURE_DETECTOR_AGAST_7_12d", "AGAST_FEATURE_DETECTOR_AGAST_7_12d", "AGAST_FEATURE_DETECTOR_AGAST_7_12d", "", 1),
    ("AGAST_FEATURE_DETECTOR_OAST_9_16", "AGAST_FEATURE_DETECTOR_OAST_9_16", "AGAST_FEATURE_DETECTOR_OAST_9_16", "", 3),
    ("AGAST_FEATURE_DETECTOR_THRESHOLD", "AGAST_FEATURE_DETECTOR_THRESHOLD", "AGAST_FEATURE_DETECTOR_THRESHOLD", "", 4),
    ("AGAST_FEATURE_DETECTOR_NONMAX_SUPPRESSION", "AGAST_FEATURE_DETECTOR_NONMAX_SUPPRESSION", "AGAST_FEATURE_DETECTOR_NONMAX_SUPPRESSION", "", 5),
)

AGAST_WORK_MODE_ITEMS = (
    ("DETECT", "DETECT", "DETECT", "", 0),
    ("COMPUTE", "COMPUTE", "COMPUTE", "CANCEL", 1),
    ("DETECT-COMPUTE", "DETECT-COMPUTE", "DETECT-COMPUTE", "CANCEL", 2),
)


class OCVLAgastFeatureDetectorNode(OCVLFeature2DNode):

    n_doc = "Wrapping class for feature detection using the AGAST method. "
    _init_method = cv2.AgastFeatureDetector_create

    def update_layout(self, context):
        self.update_sockets(context)
        updateNode(self, context)

    def update_and_init(self, context):
        InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_sockets(context)
        updateNode(self, context)

    image_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description="Input 8-bit or floating-point 32-bit, single-channel image.")
    mask_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description="Optional region of interest.")
    keypoints_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description="")

    keypoints_out = bpy.props.StringProperty(default=str(uuid.uuid4()), description="")
    descriptors_out = bpy.props.StringProperty(default=str(uuid.uuid4()), description="")

    loc_file_load = bpy.props.StringProperty(default="/", description="")
    loc_file_save = bpy.props.StringProperty(default="/", description="")
    loc_work_mode = bpy.props.EnumProperty(items=AGAST_WORK_MODE_ITEMS, default="DETECT", update=update_layout, description="")
    loc_state_mode = bpy.props.EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description="")
    loc_descriptor_size = bpy.props.IntProperty(default=0, description="")
    loc_descriptor_type = bpy.props.IntProperty(default=0, description="")
    loc_default_norm = bpy.props.IntProperty(default=0, description="")
    loc_class_repr = bpy.props.StringProperty(default="", description="")

    threshold_init = bpy.props.IntProperty(default=10, min=0, max=100, update=update_and_init, description="")
    nonmaxSuppression_init = bpy.props.BoolProperty(default=True, update=update_and_init, description="")
    type_init = bpy.props.EnumProperty(items=TYPE_ITEMS, default="AGAST_FEATURE_DETECTOR_OAST_9_16", update=update_and_init, description="")

    def init(self, context):
        super().sv_init(context)

    def wrapped_process(self):
        agast = FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

        if self.loc_work_mode == "DETECT":
            self._detect(agast)
        elif self.loc_work_mode == "COMPUTE":
            self._compute(agast)
        elif self.loc_work_mode == "DETECT-COMPUTE":
            self._detect_and_compute(agast)



