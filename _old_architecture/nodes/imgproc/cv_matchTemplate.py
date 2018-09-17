import cv2
import uuid
import numpy as np
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode, TEMPLATE_MATCH_MODE_ITEMS


class OCVLmatchTemplateNode(OCVLNode):

    _doc = _("Compares a template against overlapped image regions.")

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Image where the search is running. It must be 8-bit or 32-bit floating-point."))
    templ_in = StringProperty(name="templ_in", default=str(uuid.uuid4()),
        description=_("Searched template. It must be not greater than the source image and have the same data type."))
    mask_in = StringProperty(name="templ_in", default=str(uuid.uuid4()),
        description=_("Input mask."))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))
    result_out = StringProperty(name="result_out", default=str(uuid.uuid4()),
        description=_("Map of comparison results. It must be single-channel 32-bit floating-point."))

    def get_anchor(self):
        return self.get("anchor_in", (-1, -1))

    method_in = EnumProperty(items=TEMPLATE_MATCH_MODE_ITEMS, default='TM_CCOEFF_NORMED', update=updateNode,
        description=_("Parameter specifying the comparison method, see cv::TemplateMatchModes."))

    def sv_init(self, context):
        self.width = 150
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new('StringsSocket', "templ_in")
        self.inputs.new('StringsSocket', "mask_in")

        self.outputs.new("StringsSocket", "image_out")
        self.outputs.new("StringsSocket", "result_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in", "templ_in"])

        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'templ_in': self.get_from_props("templ_in"),
            # 'mask_in': self.get_from_props("mask_in"),
            'method_in': self.get_from_props("method_in"),
            }

        result_out = self.process_cv(fn=cv2.matchTemplate, kwargs=kwargs)
        image_out = np.copy(self.get_from_props("image_in"))
        h, w, _ = self.get_from_props("templ_in").shape
        threshold = 0.8
        loc = np.where(result_out >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(image_out, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)

        self.refresh_output_socket("result_out", result_out, is_uuid_type=True)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'method_in')


def register():
    cv_register_class(OCVLmatchTemplateNode)


def unregister():
    cv_unregister_class(OCVLmatchTemplateNode)
