import cv2
import uuid
import numpy as np
from gettext import gettext as _
from bpy.props import (
    StringProperty, BoolProperty, IntProperty, FloatProperty
)

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLgoodFeaturesToTrackNode(OCVLNode):

    _doc = _("Determines strong corners on an image.")
    _url = "http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_shi_tomasi/py_shi_tomasi.html"

    image_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Input 8-bit or floating-point 32-bit, single-channel image."))
    mask_in = StringProperty(default=str(uuid.uuid4()), update=updateNode,
        description=_("Optional region of interest."))
    maxCorners_in = IntProperty(default=25, min=1, max=1000, update=updateNode,
        description=_("Output vector of detected corners."))
    qualityLevel_in = FloatProperty(default=0.01, min=0., max=1., update=updateNode,
        description=_("Maximum number of corners to return."))
    minDistance_in = FloatProperty(default=10, min=1, max=1000, update=updateNode,
        description=_("Minimum possible Euclidean distance between the returned corners."))
    blockSize_in = IntProperty(default=3, min=1, max=100, update=updateNode,
        description=_("Size of an average block for computing a derivative covariation matrix over each pixel neighborhood."))
    gradientSize_in = IntProperty(default=3, min=1, max=100, update=updateNode,
        description="")
    useHarrisDetector_in = BoolProperty(default=False, update=updateNode,
        description=_("Parameter indicating whether to use a Harris detector (see cornerHarris) or cornerMinEigenVal."))
    k_in = FloatProperty(default=0.04, min=0.01, max=1., update=updateNode,
        description="Free parameter of the Harris detector.")

    corners_out = StringProperty(name="corners_out", default=str(uuid.uuid4()),
        description=_("Output vector of detected corners."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output vector of detected corners."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "mask_in")
        self.inputs.new("StringsSocket", "maxCorners_in").prop_name = "maxCorners_in"
        self.inputs.new("StringsSocket", "qualityLevel_in").prop_name = "qualityLevel_in"
        self.inputs.new("StringsSocket", "minDistance_in").prop_name = "minDistance_in"
        self.inputs.new("StringsSocket", "blockSize_in").prop_name = "blockSize_in"
        self.inputs.new("StringsSocket", "gradientSize_in").prop_name = "gradientSize_in"
        self.inputs.new("StringsSocket", "useHarrisDetector_in").prop_name = "useHarrisDetector_in"
        self.inputs.new("StringsSocket", "k_in").prop_name = "k_in"

        self.outputs.new("StringsSocket", "corners_out")
        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'mask_in': self.get_from_props("mask_in"),
            'maxCorners_in': self.get_from_props("maxCorners_in"),
            'qualityLevel_in': self.get_from_props("qualityLevel_in"),
            'minDistance_in': self.get_from_props("minDistance_in"),
            'blockSize_in': self.get_from_props("blockSize_in"),
            'gradientSize_in': self.get_from_props("gradientSize_in"),
            'useHarrisDetector_in': self.get_from_props("useHarrisDetector_in"),
            'k_in': self.get_from_props("k_in"),
            }

        if isinstance(kwargs['mask_in'], str):
            kwargs['mask_in'] = np.ones(shape=kwargs['image_in'].shape, dtype=np.uint8)

        corners_out = self.process_cv(fn=cv2.goodFeaturesToTrack, kwargs=kwargs)
        self.refresh_output_socket("corners_out", corners_out, is_uuid_type=True)

        corners = np.int0(corners_out)
        image_out = kwargs['image_in'].copy()

        for i in corners:
            x, y = i.ravel()
            cv2.circle(image_out, (x, y), 3, 255, -1)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)


def register():
    cv_register_class(OCVLgoodFeaturesToTrackNode)


def unregister():
    cv_unregister_class(OCVLgoodFeaturesToTrackNode)
