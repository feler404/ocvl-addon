import cv2
import bpy
from ocvl.core.globals import FEATURE2D_INSTANCES_DICT
from ocvl.core.node_base import OCVLNodeBase, update_node
from ocvl.nodes.objdetect.abc_Feature2D import OCVLFeature2DDetectorMixIn
from ocvl.operatores.abc import OCVL_OT_InitFeature2DOperator


SBD_WORK_MODE_ITEMS = (
    ("DETECT", "DETECT", "DETECT", "CANCEL", 0),
    ("COMPUTE", "COMPUTE", "COMPUTE", "", 1),
    ("DETECT-COMPUTE", "DETECT-COMPUTE", "DETECT-COMPUTE", "CANCEL", 2),
)


class OCVLSimpleBlobDetectorNode(OCVLFeature2DDetectorMixIn, OCVLNodeBase):
    # n_development_status = "ALPHA"

    n_doc = "Class for extracting blobs from an image."
    _init_method = cv2.SimpleBlobDetector_create

    def update_and_init(self, context):
        OCVL_OT_InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_layout(context)

    blobColor_init: bpy.props.IntProperty(default=0, min=0, update=update_and_init)
    filterByArea_init: bpy.props.BoolProperty(default=True, update=update_and_init)
    filterByCircularity_init: bpy.props.BoolProperty(default=False, update=update_and_init)
    filterByColor_init: bpy.props.BoolProperty(default=True, update=update_and_init)
    filterByConvexity_init: bpy.props.BoolProperty(default=True, update=update_and_init)
    filterByInertia_init: bpy.props.BoolProperty(default=True, update=update_and_init)

    minArea_init: bpy.props.FloatProperty(default=25.0, min=1, max=100000, update=update_and_init)
    maxArea_init: bpy.props.FloatProperty(default=5000.0, min=1, max=100000, update=update_and_init)

    minConvexity_init: bpy.props.FloatProperty(default=0.95, min=0.01, max=100000, update=update_and_init)
    maxConvexity_init: bpy.props.FloatProperty(default=100000, min=0.01, update=update_and_init)

    minCircularity_init: bpy.props.FloatProperty(default=0.8, min=0.01, update=update_and_init)
    maxCircularity_init: bpy.props.FloatProperty(default=100000, min=0.01, update=update_and_init)

    minInertiaRatio_init: bpy.props.FloatProperty(default=0.1, min=0.01, update=update_and_init)
    maxInertiaRatio_init: bpy.props.FloatProperty(default=100000, min=0.01, update=update_and_init)

    minThreshold_init: bpy.props.FloatProperty(default=50.0, min=1, max=1000, update=update_and_init)
    maxThreshold_init: bpy.props.FloatProperty(default=220.0, min=1, max=1000, update=update_and_init)

    thresholdStep_init: bpy.props.FloatProperty(default=10.0, min=1, max=1000, update=update_and_init)

    def _init_method(self, *args, **kwargs):
        params = cv2.SimpleBlobDetector_Params()
        for key in kwargs:
            setattr(params, key, kwargs[key])

        instance = cv2.SimpleBlobDetector_create(params)
        return instance

    def init(self, context):
        super().init(context)

    def wrapped_process(self):
        instance = FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

        if self.loc_work_mode == "DETECT":
            self._detect(instance)
        elif self.loc_work_mode == "COMPUTE":
            self._compute(instance)
        elif self.loc_work_mode == "DETECT-COMPUTE":
            self._detect_and_compute(instance)
