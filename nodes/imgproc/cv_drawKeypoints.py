import cv2
import uuid
import numpy as np
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty


from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLdrawKeypointsNode(OCVLNode):

    _doc = _("Class for extracting keypoints and computing descriptors using the Scale Invariant Feature Transform (SIFT) algorithm by D. Lowe")
    _url = "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.html"

    image_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Source image."))

    keypoints_in = IntProperty(default=0, min=0, max=100, update=updateNode,
        description=_("Keypoints from the source image."))
    # color_in = FloatProperty(default=1.6, min=0.1, max=5., update=updateNode,
    #     description="The sigma of the Gaussian applied to the input image at the octave #0.")
    # flags_in =

    outImage_out = StringProperty(default=str(uuid.uuid4()),
        description=_("Output image."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "keypoints_in").prop_name = "keypoints_in"

        self.outputs.new("StringsSocket", "outImage_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'outImage': np.zeros(self.get_from_props("image_in").shape),
            'keypoints_in': self.get_from_props("keypoints_in"),
            'flags_in': cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            }

        outImage_out = self.process_cv(fn=cv2.drawKeypoints, kwargs=kwargs)
        self.refresh_output_socket("outImage_out", outImage_out, is_uuid_type=True)


def register():
    cv_register_class(OCVLdrawKeypointsNode)


def unregister():
    cv_unregister_class(OCVLdrawKeypointsNode)
