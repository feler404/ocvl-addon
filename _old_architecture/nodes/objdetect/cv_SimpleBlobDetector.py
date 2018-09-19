import cv2
import uuid

import bpy

from .abc_Feature2D import OCVLFeature2DNode, WORK_MODE_ITEMS, STATE_MODE_ITEMS
from ...operatores.abc import InitFeature2DOperator
from ...globals import FEATURE2D_INSTANCES_DICT
from ocvl.core.node_base import OCVLNodeBase, update_node


SBD_WORK_MODE_ITEMS = (
    ("DETECT", "DETECT", "DETECT", "CANCEL", 0),
    ("COMPUTE", "COMPUTE", "COMPUTE", "", 1),
    ("DETECT-COMPUTE", "DETECT-COMPUTE", "DETECT-COMPUTE", "CANCEL", 2),
)


class OCVLSimpleBlobDetectorNode(OCVLFeature2DNode):

    n_doc = _("Class for extracting blobs from an image.")
    _init_method = cv2.SimpleBlobDetector_create

    def update_layout(self, context):
        self.update_sockets(context)
        update_node(self, context)

    def update_and_init(self, context):
        InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_sockets(context)
        update_node(self, context)

    image_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description=_("Input 8-bit or floating-point 32-bit, single-channel image.")
    mask_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description=_("Optional region of interest.")
    keypoints_in = bpy.props.StringProperty(default=str(uuid.uuid4()), description=_("")

    keypoints_out = bpy.props.StringProperty(default=str(uuid.uuid4()), description=_("")
    descriptors_out = bpy.props.StringProperty(default=str(uuid.uuid4()), description=_("")

    loc_file_load = bpy.props.StringProperty(default="/", description=_("")
    loc_file_save = bpy.props.StringProperty(default="/", description=_("")
    loc_work_mode = bpy.props.EnumProperty(items=SBD_WORK_MODE_ITEMS, default="COMPUTE", update=update_layout, description=_("")
    loc_state_mode = bpy.props.EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description=_("")
    loc_descriptor_size = bpy.props.IntProperty(default=0, description=_("")
    loc_descriptor_type = bpy.props.IntProperty(default=0, description=_("")
    loc_default_norm = bpy.props.IntProperty(default=0, description=_("")
    loc_class_repr = bpy.props.StringProperty(default="", description=_("")

    # nfeatures_init = bpy.props.IntProperty(default=0, min=0, max=100, update=update_and_init,
    #     description=_("The number of best features to retain.")
    # nOctaveLayers_init = bpy.props.IntProperty(default=3, min=1, max=3, update=update_and_init,
    #     description=_("The number of layers in each octave.")
    # contrastThreshold_init = bpy.props.FloatProperty(default=0.04, min=0.01, max=0.1, update=update_and_init,
    #     description=_("The contrast threshold used to filter out weak features in semi-uniform (low-contrast) regions.")
    # edgeThreshold_init = bpy.props.FloatProperty(default=10, min=0.1, max=100, update=update_and_init,
    #     description=_("Size of an average block for computing a derivative covariation matrix over each pixel neighborhood.")
    # sigma_init = bpy.props.FloatProperty(default=1.6, min=0.1, max=5., update=update_and_init,
    #     description="The sigma of the Gaussian applied to the input image at the octave #0.")

    def init(self, context):
        super().sv_init(context)

    def wrapped_process(self):
        instance = FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

        if self.loc_work_mode == "DETECT":
            pass
            # self._detect(instance)
        elif self.loc_work_mode == "COMPUTE":
            self._compute(instance)
        elif self.loc_work_mode == "DETECT-COMPUTE":
            pass
            # self._detect_and_compute(instance)
