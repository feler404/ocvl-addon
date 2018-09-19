import cv2
import uuid

import bpy

from .abc_Feature2D import OCVLFeature2DNode, WORK_MODE_ITEMS, STATE_MODE_ITEMS
from ...operatores.abc import InitFeature2DOperator
from ...globals import FEATURE2D_INSTANCES_DICT
from ocvl.core.node_base import OCVLNodeBase, update_node


NORM_ITEMS = (
    ("DAISY_NRM_NONE", "DAISY_NRM_NONE", "DAISY_NRM_NONE", "", 0),
    ("DAISY_NRM_PARTIAL", "DAISY_NRM_PARTIAL", "DAISY_NRM_PARTIAL", "", 1),
    ("DAISY_NRM_FULL", "DAISY_NRM_FULL", "DAISY_NRM_FULL", "", 2),
    ("DAISY_NRM_SIFT", "DAISY_NRM_SIFT", "DAISY_NRM_SIFT", "", 3),
)

DAISY_WORK_MODE_ITEMS = (
    ("DETECT", "DETECT", "DETECT", "CANCEL", 0),
    ("COMPUTE", "COMPUTE", "COMPUTE", "", 1),
    ("DETECT-COMPUTE", "DETECT-COMPUTE", "DETECT-COMPUTE", "CANCEL", 2),
)

class OCVLDAISYNode(OCVLFeature2DNode):

    n_doc = "Class implementing DAISY descriptor, described in [178]."
    _init_method = cv2.xfeatures2d.DAISY_create

    def update_layout(self, context):
        self.update_sockets(context)
        update_node(self, context)

    def update_and_init(self, context):
        InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_sockets(context)
        update_node(self, context)

    image_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description="Input 8-bit or floating-point 32-bit, single-channel image.")
    mask_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description="Optional region of interest.")
    keypoints_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description="")

    keypoints_out = bpy.props.StringProperty(default=str(uuid.uuid4()), description="")
    descriptors_out = bpy.props.StringProperty(default=str(uuid.uuid4()), description="")

    loc_file_load = bpy.props.StringProperty(default="/", description="")
    loc_file_save = bpy.props.StringProperty(default="/", description="")
    loc_work_mode = bpy.props.EnumProperty(items=DAISY_WORK_MODE_ITEMS, default="COMPUTE", update=update_layout, description="")
    loc_state_mode = bpy.props.EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description="")
    loc_descriptor_size = bpy.props.IntProperty(default=0, description="")
    loc_descriptor_type = bpy.props.IntProperty(default=0, description="")
    loc_default_norm = bpy.props.IntProperty(default=0, description="")
    loc_class_repr = bpy.props.StringProperty(default="", description="")

    radius_init = bpy.props.FloatProperty(default=15, min=0.1, max=100, update=update_and_init, description="")
    q_radius_init = bpy.props.IntProperty(default=3, min=0, max=100, update=update_and_init, description="")
    q_theta_init = bpy.props.IntProperty(default=8, min=0, max=100, update=update_and_init, description="")
    q_hist_init = bpy.props.IntProperty(default=8, min=0, max=100, update=update_and_init, description="")
    norm_init = bpy.props.EnumProperty(items=NORM_ITEMS, default="DAISY_NRM_NONE", update=update_and_init, description="")
    interpolation_init = bpy.props.BoolProperty(default=True, update=update_and_init, description="")
    use_orientation_init = bpy.props.BoolProperty(default=False, update=update_and_init, description="")

    def init(self, context):
        super().sv_init(context)

    def wrapped_process(self):
        instance = FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

        if self.loc_work_mode == "DETECT":
            self._detect(instance)
        elif self.loc_work_mode == "COMPUTE":
            self._compute(instance)
        elif self.loc_work_mode == "DETECT-COMPUTE":
            self._detect_and_compute(instance)
