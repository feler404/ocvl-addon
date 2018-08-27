import cv2
import uuid
import numpy as np
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


NORM_TYPE_ITEMS = (
    ("NORM_L1", "NORM_L1", "NORM_L1", "", 0),
    ("NORM_L2", "NORM_L2", "NORM_L2", "", 1),
    ("NORM_HAMMING", "NORM_HAMMING", "NORM_HAMMING", "", 2),
    ("NORM_HAMMING2", "NORM_HAMMING2", "NORM_HAMMING2", "", 3),
)


class OCVLBFMatcherNode(OCVLNode):

    _doc = _("Brute-force matcher create method.")
    _url = "https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html"

    queryDescriptors_in = StringProperty(default=str(uuid.uuid4()),
        description=_("Query set of descriptors."))
    trainDescriptors_in = StringProperty(default=str(uuid.uuid4()), update=updateNode,
        description=_(""))

    normType_in = EnumProperty(default="NORM_HAMMING", items=NORM_TYPE_ITEMS, update=updateNode,
        description=_("One of NORM_L1, NORM_L2, NORM_HAMMING, NORM_HAMMING2."))
    crossCheck_in = BoolProperty(default=False, update=updateNode,
        description=_("If it is false, this is will be default BFMatcher behaviour when it finds the k nearest neighbors for each query descriptor."))

    matches_out = StringProperty(default=str(uuid.uuid4()),
        description=_(""))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "queryDescriptors_in")
        self.inputs.new("StringsSocket", "trainDescriptors_in")
        self.inputs.new("StringsSocket", "crossCheck_in").prop_name = "crossCheck_in"

        self.outputs.new("StringsSocket", "matches_out")

    def wrapped_process(self):
        self.check_input_requirements(["queryDescriptors_in", "trainDescriptors_in"])

        kwargs_init = self.clean_kwargs({

            })

        kwargs_detect = self.clean_kwargs({
            "queryDescriptors_in": self.get_from_props("queryDescriptors_in"),
        })

        # if isinstance(kwargs_detect['mask'], str):
        #     kwargs_detect['mask'] = np.ones(kwargs_detect['image'].shape)

        bfm = cv2.BFMatcher_create(**kwargs_init)
        bfm.add(self.get_from_props("trainDescriptors_in"))
        matches_out = self.process_cv(fn=bfm.match, kwargs=kwargs_detect)
        self.refresh_output_socket("matches_out", matches_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, prop_name='scoreType_in')


def register():
    cv_register_class(OCVLBFMatcherNode)


def unregister():
    cv_unregister_class(OCVLBFMatcherNode)
