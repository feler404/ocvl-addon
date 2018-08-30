import cv2
import uuid
import numpy as np
from gettext import gettext as _
from bpy.props import (
    StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty,
    BoolVectorProperty)

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLdrawMatchesNode(OCVLNode):
    bl_flags_list = 'DRAW_MATCHES_FLAGS_DEFAULT, DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG, DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS'
    _doc = _("This is an overloaded member function, provided for convenience. It differs from the above function only in what argument(s) it accepts.")

    img1_in = StringProperty(default=str(uuid.uuid4()), description=_("Source image."))
    img2_in = StringProperty(default=str(uuid.uuid4()), description=_("Source image."))
    keypoints1_in = StringProperty(default=str(uuid.uuid4()), description=_("Keypoints from the first source image."))
    keypoints2_in = StringProperty(default=str(uuid.uuid4()), description=_("Keypoints from the first source image."))
    matches1to2_in = StringProperty(default=str(uuid.uuid4()), description=_("Matches from the first image to the second one."))
    matchesMask_in = StringProperty(default=str(uuid.uuid4()), description=_("Mask determining which matches are drawn. If the mask is empty, all matches are drawn."))

    matchColor_in = FloatVectorProperty(update=updateNode, name='matchColor', default=(.3, .3, .2, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR')
    singlePointColor_in = FloatVectorProperty(update=updateNode, name='singlePointColor_in', default=(.3, .3, .2, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR')
    loc_max_distance_in = IntProperty(default=500, min=100, max=10000, update=updateNode)

    flags_in = BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")), update=updateNode, subtype="NONE", description=bl_flags_list)

    outImg_out = StringProperty(default=str(uuid.uuid4()), description=_("Output image."))


    def sv_init(self, context):
        self.inputs.new("StringsSocket", "img1_in")
        self.inputs.new("StringsSocket", "img2_in")
        self.inputs.new("StringsSocket", "keypoints1_in")
        self.inputs.new("StringsSocket", "keypoints2_in")
        self.inputs.new("StringsSocket", "matches1to2_in")
        self.inputs.new("StringsSocket", "matchesMask_in")
        self.inputs.new("StringsSocket", "matchColor_in").prop_name = "matchColor_in"
        self.inputs.new("StringsSocket", "singlePointColor_in").prop_name = "singlePointColor_in"
        self.inputs.new("StringsSocket", "loc_max_distance_in").prop_name = "loc_max_distance_in"

        self.outputs.new("StringsSocket", "outImg_out")

    def wrapped_process(self):
        self.check_input_requirements(["img1_in", "img2_in", "keypoints1_in", "keypoints2_in", "matches1to2_in"])

        img1 = self.get_from_props("img1_in")
        img2 = self.get_from_props("img2_in")
        keypoints1_in = self.get_from_props("keypoints1_in")
        keypoints2_in = self.get_from_props("keypoints2_in")
        matches1to2_in = self.get_from_props("matches1to2_in")
        loc_max_distance_in = self.get_from_props("loc_max_distance_in")

        good = []
        for dmatch in matches1to2_in:
            if dmatch.distance < loc_max_distance_in:
                good.append(dmatch)

        draw_params = {
            'matchColor': self.get_from_props("matchColor_in"),
            'singlePointColor': self.get_from_props("singlePointColor_in"),
            'flags': self.get_from_props("flags_in"),
            'matchesMask': None,  # self.get_from_props("matchesMask_in")
        }
        # outImg_out = self.process_cv(fn=cv2.drawMatches, kwargs=kwargs)
        outImg_out = cv2.drawMatches(img1, keypoints1_in, img2, keypoints2_in, good, None, **draw_params)
        self.refresh_output_socket("outImg_out", outImg_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")


def register():
    cv_register_class(OCVLdrawMatchesNode)


def unregister():
    cv_unregister_class(OCVLdrawMatchesNode)
