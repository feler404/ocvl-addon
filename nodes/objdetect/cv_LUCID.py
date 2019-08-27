import bpy
import cv2
from ocvl.core.globals import FEATURE2D_INSTANCES_DICT
from ocvl.core.node_base import OCVLNodeBase, update_node
from ocvl.nodes.objdetect.abc_Feature2D import OCVLFeature2DCalculatorDMixIn
from ocvl.operatores.abc import OCVL_OT_InitFeature2DOperator


class OCVLLUCIDNode(OCVLFeature2DCalculatorDMixIn, OCVLNodeBase):

    n_doc = "Class implementing the locally uniform comparison image descriptor, described in [216]."
    _init_method = cv2.xfeatures2d.LUCID_create

    def update_and_init(self, context):
        OCVL_OT_InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_sockets(context)
        update_node(self, context)

    lucid_kernel_init: bpy.props.IntProperty(default=1, min=1, max=9, update=update_and_init, description="")
    blur_kernel_init: bpy.props.IntProperty(default=1, min=1, max=9, update=update_and_init, description="")

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
