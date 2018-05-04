import bpy
import cv2
import uuid
import random
import numpy as np
from logging import getLogger
from bpy.props import EnumProperty, StringProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode
from ...auth import ocvl_auth



class OCVLROINode(OCVLNode):
    ''' Get region of image.
        .   @param img Image.
        .   @param pt1 First point of the ROI segment.
        .   @param pt2 Second point of the ROI segment.
    '''

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))
    image_roi_out = StringProperty(name="image_roi_out", default=str(uuid.uuid4()))

    pt1_in = IntVectorProperty(default=(0, 0), size=2, update=updateNode,
        description="First point of the line segment.")
    pt2_in = IntVectorProperty(default=(1, 1), size=2, update=updateNode,
        description="First point of the line segment.")

    def sv_init(self, context):
        self.width = 200
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "pt1_in").prop_name = 'pt1_in'
        self.inputs.new('StringsSocket', "pt2_in").prop_name = 'pt2_in'

        self.outputs.new("StringsSocket", "image_out")
        self.outputs.new("StringsSocket", "image_roi_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        image_in = self.get_from_props("image_in")
        pt1_in = self.get_from_props("pt1_in")
        pt2_in = self.get_from_props("pt2_in")

        image_roi_out = image_in[pt1_in[1]:pt2_in[1], pt1_in[0]:pt2_in[0]]
        image_out = image_in[:]
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)
        self.refresh_output_socket("image_roi_out", image_roi_out, is_uuid_type=True)



if ocvl_auth.ocvl_pro_version_auth:
    pass
    # from ...extend.laboratory.ta_ROI import OCVLROINode


def register():
    cv_register_class(OCVLROINode)


def unregister():
    cv_unregister_class(OCVLROINode)
