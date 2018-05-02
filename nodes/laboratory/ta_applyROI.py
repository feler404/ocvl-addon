import bpy
import cv2
import uuid
import random
import numpy as np
from logging import getLogger
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, DEVELOP_STATE_BETA
from ...auth import ocvl_auth


class OCVLSimpleApplyROINode(OCVLNode):

    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Insert ROI to other image.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_roi_in = StringProperty(name="image_roi_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))

    pt1_in = IntVectorProperty(default=(0, 0), size=2, min=0, update=updateNode,
        description=_("Upper left corner ROI inserting."))

    def sv_init(self, context):
        self.width = 200
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "image_roi_in")
        self.inputs.new('StringsSocket', "pt1_in").prop_name = 'pt1_in'

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in", "image_roi_in"])

        image_in = self.get_from_props("image_in")
        image_roi_in = self.get_from_props("image_roi_in")
        pt1_in = self.get_from_props("pt1_in")

        image_out = image_in.copy()
        image_out[pt1_in[0]:image_roi_in.shape[0] + pt1_in[0], pt1_in[1]:image_roi_in.shape[1] + pt1_in[1]] = image_roi_in
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)


if ocvl_auth.ocvl_ext:
    # from ...extend.laboratory.ta_ROI import OCVLROINode

    def register():
        # cv_register_class(OCVLAapplyROINode)
        cv_register_class(OCVLSimpleApplyROINode)


    def unregister():
        cv_unregister_class(OCVLSimpleApplyROINode)
        # cv_unregister_class(OCVLAapplyROINode)
