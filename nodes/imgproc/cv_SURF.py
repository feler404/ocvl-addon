import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty


from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLSURFNode(OCVLNode):

    _doc = _("Class for extracting Speeded Up Robust Features from an image.")
    _url = "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html"

    image_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Input 8-bit or floating-point 32-bit, single-channel image."))
    mask_in = StringProperty(default=str(uuid.uuid4()), update=updateNode,
        description=_("Optional region of interest."))

    hessianThreshold_in = FloatProperty(default=100, min=10, max=1000, step=100, update=updateNode,
        description=_("Threshold for hessian keypoint detector used in SURF."))
    nOctaves_in = IntProperty(default=4, min=1, max=10, update=updateNode,
        description=_("Number of pyramid octaves the keypoint detector will use."))
    nOctaveLayers_in = IntProperty(default=3, min=1, max=3, update=updateNode,
        description=_("Number of octave layers within each octave."))
    extended_in = BoolProperty(default=False, update=updateNode,
        description=_("Extended descriptor flag (true - use extended 128-element descriptors; false - use 64-element descriptors)."))
    upright_in = BoolProperty(default=False, update=updateNode,
        description=_("	Up-right or rotated features flag (true - do not compute orientation of features; false - compute orientation)."))

    keypoints_out = StringProperty(default=str(uuid.uuid4()),
        description=_("Output vector of detected keypoints."))
    descriptors_out = StringProperty(default=str(uuid.uuid4()),
        description=_("Output vector of detected descriptors."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "mask_in")
        self.inputs.new("StringsSocket", "hessianThreshold_in").prop_name = "hessianThreshold_in"
        self.inputs.new("StringsSocket", "nOctaves_in").prop_name = "nOctaves_in"
        self.inputs.new("StringsSocket", "nOctaveLayers_in").prop_name = "nOctaveLayers_in"
        self.inputs.new("StringsSocket", "extended_in").prop_name = "extended_in"
        self.inputs.new("StringsSocket", "upright_in").prop_name = "upright_in"

        self.outputs.new("StringsSocket", "keypoints_out")
        self.outputs.new("StringsSocket", "descriptors_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs_init = {
            'hessianThreshold': self.get_from_props("hessianThreshold_in"),
            'nOctaves': self.get_from_props("nOctaves_in"),
            'nOctaveLayers': self.get_from_props("nOctaveLayers_in"),
            'extended': self.get_from_props("extended_in"),
            'upright': self.get_from_props("upright_in"),
            }

        kwargs_detect = {
            'image': self.get_from_props("image_in"),
            'mask': None  # self.get_from_props("mask_in"),
        }

        surf = cv2.xfeatures2d.SURF_create(**kwargs_init)
        keypoints_out, descriptors_out = self.process_cv(fn=surf.detectAndCompute, kwargs=kwargs_detect)
        self.refresh_output_socket("keypoints_out", keypoints_out, is_uuid_type=True)
        self.refresh_output_socket("descriptors_out", descriptors_out, is_uuid_type=True)


def register():
    cv_register_class(OCVLSURFNode)


def unregister():
    cv_unregister_class(OCVLSURFNode)
