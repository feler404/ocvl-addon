import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty


from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLSIFTNode(OCVLNode):

    _doc = _("Class for extracting keypoints and computing descriptors using the Scale Invariant Feature Transform (SIFT) algorithm by D. Lowe")
    _url = "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.html"

    image_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Input 8-bit or floating-point 32-bit, single-channel image."))
    mask_in = StringProperty(default=str(uuid.uuid4()), update=updateNode,
        description=_("Optional region of interest."))

    nfeatures_in = IntProperty(default=0, min=0, max=100, update=updateNode,
        description=_("The number of best features to retain."))
    nOctaveLayers_in = IntProperty(default=3, min=1, max=3, update=updateNode,
        description=_("The number of layers in each octave."))
    contrastThreshold_in = FloatProperty(default=0.04, min=0.01, max=0.1, update=updateNode,
        description=_("The contrast threshold used to filter out weak features in semi-uniform (low-contrast) regions."))
    edgeThreshold_in = FloatProperty(default=10, min=0.1, max=100, update=updateNode,
        description=_("Size of an average block for computing a derivative covariation matrix over each pixel neighborhood."))
    sigma_in = FloatProperty(default=1.6, min=0.1, max=5., update=updateNode,
        description="The sigma of the Gaussian applied to the input image at the octave #0.")

    keypoints_out = StringProperty(default=str(uuid.uuid4()),
        description=_("Output vector of detected keypoints."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "mask_in")
        self.inputs.new("StringsSocket", "nfeatures_in").prop_name = "nfeatures_in"
        self.inputs.new("StringsSocket", "nOctaveLayers_in").prop_name = "nOctaveLayers_in"
        self.inputs.new("StringsSocket", "contrastThreshold_in").prop_name = "contrastThreshold_in"
        self.inputs.new("StringsSocket", "edgeThreshold_in").prop_name = "edgeThreshold_in"
        self.inputs.new("StringsSocket", "sigma_in").prop_name = "sigma_in"

        self.outputs.new("StringsSocket", "keypoints_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs_init = {
            'nfeatures': self.get_from_props("nfeatures_in"),
            'nOctaveLayers': self.get_from_props("nOctaveLayers_in"),
            'contrastThreshold': self.get_from_props("contrastThreshold_in"),
            'edgeThreshold': self.get_from_props("edgeThreshold_in"),
            'sigma': self.get_from_props("sigma_in"),
            }

        kwargs_detect = {
            'images': [self.get_from_props("image_in")],
            'masks': None,
        }

        sift = cv2.xfeatures2d.SIFT_create(**kwargs_init)
        keypoints_out = self.process_cv(fn=sift.detect, kwargs=kwargs_detect)
        self.refresh_output_socket("keypoints_out", keypoints_out, is_uuid_type=True)


def register():
    cv_register_class(OCVLSIFTNode)


def unregister():
    cv_unregister_class(OCVLSIFTNode)
