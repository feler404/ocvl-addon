import cv2
from ocvl.core.globals import FEATURE2D_INSTANCES_DICT
from ocvl.core.node_base import OCVLNodeBase
from ocvl.nodes.objdetect.abc_Feature2D import OCVLFeature2DCalculatorDMixIn
from ocvl.operatores.abc import OCVL_OT_InitFeature2DOperator


class OCVLBoostDescNode(OCVLFeature2DCalculatorDMixIn, OCVLNodeBase):

    n_doc = "Class implementing BoostDesc (Learning Image Descriptors with Boosting), described in [171] and [172]."
    n_development_status = "BETA"
    _init_method = cv2.xfeatures2d.BoostDesc_create

    def update_and_init(self, context):
        OCVL_OT_InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_layout(context)

    # desc_init: bpy.props.EnumProperty()
    # use_scale_orientation_init: bpy.props.BoolProperty()
    # scale_factor_init: bpy.props.FloatProperty()

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
