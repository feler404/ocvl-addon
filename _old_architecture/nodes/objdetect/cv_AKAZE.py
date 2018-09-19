import cv2
import uuid

import bpy

from .abc_Feature2D import OCVLFeature2DNode, WORK_MODE_ITEMS, STATE_MODE_ITEMS
from ...operatores.abc import InitFeature2DOperator
from ...globals import FEATURE2D_INSTANCES_DICT
from ocvl.core.node_base import OCVLNodeBase, update_node

DESCRIPTOR_TYPE_ITEMS = (
    ("AKAZE_DESCRIPTOR_KAZE_UPRIGHT", "AKAZE_DESCRIPTOR_KAZE_UPRIGHT", "AKAZE_DESCRIPTOR_KAZE_UPRIGHT", "", 0),
    ("AKAZE_DESCRIPTOR_KAZE", "AKAZE_DESCRIPTOR_KAZE", "AKAZE_DESCRIPTOR_KAZE", "", 1),
    ("AKAZE_DESCRIPTOR_MLDB_UPRIGHT", "AKAZE_DESCRIPTOR_MLDB_UPRIGHT", "AKAZE_DESCRIPTOR_MLDB_UPRIGHT", "", 2),
    ("AKAZE_DESCRIPTOR_MLDB", "AKAZE_DESCRIPTOR_MLDB", "AKAZE_DESCRIPTOR_MLDB", "", 3),
)

DIFFUSIVITY_TYPE_ITEMS = (
    ("AKAZE_DIFF_PM_G1", "AKAZE_DIFF_PM_G1", "AKAZE_DIFF_PM_G1", "", 0),
    ("AKAZE_DIFF_PM_G2", "AKAZE_DIFF_PM_G2", "AKAZE_DIFF_PM_G2", "", 1),
    ("AKAZE_DIFF_WEICKERT", "AKAZE_DIFF_WEICKERT", "AKAZE_DIFF_WEICKERT", "", 2),
    ("AKAZE_DIFF_CHARBONNIER", "AKAZE_DIFF_CHARBONNIER", "AKAZE_DIFF_CHARBONNIER", "", 3),
)


class OCVLAKAZENode(OCVLFeature2DNode):

    n_doc = "Class implementing the AKAZE keypoint detector and descriptor extractor, described in [5]."
    _init_method = cv2.AKAZE_create

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
    loc_work_mode = bpy.props.EnumProperty(items=WORK_MODE_ITEMS, default="DETECT-COMPUTE", update=update_layout, description="")
    loc_state_mode = bpy.props.EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description="")
    loc_descriptor_size = bpy.props.IntProperty(default=0, description="")
    loc_descriptor_type = bpy.props.IntProperty(default=0, description="")
    loc_default_norm = bpy.props.IntProperty(default=0, description="")
    loc_class_repr = bpy.props.StringProperty(default="", description="")

    descriptor_type_init = bpy.props.EnumProperty(items=DESCRIPTOR_TYPE_ITEMS, default="AKAZE_DESCRIPTOR_MLDB", update=update_and_init, description="")
    descriptor_size_init = bpy.props.IntProperty(default=0, min=0, max=32, description="")
    descriptor_channels_init = bpy.props.IntProperty(default=3, min=1, max=3, description="")
    threshold_init = bpy.props.FloatProperty(default=0.001, min=0.0001, max=0.9999, description="")
    nOctaves_init = bpy.props.IntProperty(default=4, min=1, max=10, description="")
    nOctaveLayers_init = bpy.props.IntProperty(default=4, min=1, max=10, description="")
    diffusivity = bpy.props.EnumProperty(items=DIFFUSIVITY_TYPE_ITEMS, default="AKAZE_DIFF_PM_G2", description="")

    def init(self, context):
        super().sv_init(context)

    def wrapped_process(self):
        sift = FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

        if self.loc_work_mode == "DETECT":
            self._detect(sift)
        elif self.loc_work_mode == "COMPUTE":
            self._compute(sift)
        elif self.loc_work_mode == "DETECT-COMPUTE":
            self._detect_and_compute(sift)



