import cv2
import uuid

import bpy

from .abc_Feature2D import OCVLFeature2DNode, WORK_MODE_ITEMS, STATE_MODE_ITEMS
from ...operatores.abc import InitFeature2DOperator
from ...globals import FEATURE2D_INSTANCES_DICT
from ocvl.core.node_base import OCVLNodeBase, update_node


BYTES_ITEMS = (
    ("16", "16", "16", "", 0),
    ("32", "32", "32", "", 1),
    ("64", "64", "64", "", 2),
)

BDE_WORK_MODE_ITEMS = (
    ("DETECT", "DETECT", "DETECT", "", 0),
    ("COMPUTE", "COMPUTE", "COMPUTE", "", 1),
    ("DETECT-COMPUTE", "DETECT-COMPUTE", "DETECT-COMPUTE", "", 2),
)

class OCVLBRISKNode(OCVLFeature2DNode):

    n_doc = "Class implementing the BRISK keypoint detector and descriptor extractor, described in [LCS11]."
    _url = "https://docs.opencv.org/3.0-beta/modules/features2d/doc/feature_detection_and_description.html?highlight=brisk#BRISK%20:%20public%20Feature2D"
    _init_method = cv2.BRISK_create

    def update_layout(self, context):
        self.update_sockets(context)
        update_node(self, context)

    def update_and_init(self, context):
        InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_layout(context)

    image_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description="Input 8-bit or floating-point 32-bit, single-channel image.")
    mask_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description="Optional region of interest.")
    keypoints_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description="")

    keypoints_out = bpy.props.StringProperty(default=str(uuid.uuid4()), description="")
    descriptors_out = bpy.props.StringProperty(default=str(uuid.uuid4()), description="")

    loc_file_load = bpy.props.StringProperty(default="/", description="")
    loc_file_save = bpy.props.StringProperty(default="/", description="")
    loc_work_mode = bpy.props.EnumProperty(items=BDE_WORK_MODE_ITEMS, default="COMPUTE", update=update_layout, description="")
    loc_state_mode = bpy.props.EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description="")
    loc_descriptor_size = bpy.props.IntProperty(default=0, description="")
    loc_descriptor_type = bpy.props.IntProperty(default=0, description="")
    loc_default_norm = bpy.props.IntProperty(default=0, description="")
    loc_class_repr = bpy.props.StringProperty(default="", description="")

    thresh_init = bpy.props.IntProperty(default=30, min=5, max=100, update=update_and_init)
    octaves_init = bpy.props.IntProperty(default=3, min=1, max=10, update=update_and_init)
    patternScale_init = bpy.props.IntProperty(default=1.0, min=0.1, max=10., update=update_and_init)

    def init(self, context):
        super().sv_init(context)

    def wrapped_process(self):
        brisk = FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

        if self.loc_work_mode == "DETECT":
            self._detect(brisk)
        elif self.loc_work_mode == "COMPUTE":
            self._compute(brisk)
        elif self.loc_work_mode == "DETECT-COMPUTE":
            self._detect_and_compute(brisk)
