import cv2
import uuid
import numpy as np
from bpy.props import EnumProperty, StringProperty

from ...extend.utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode, TEMPLATE_MATCH_MODE_ITEMS


class OCVLmatchTemplateNode(OCVLNode):
    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    templ_in = StringProperty(name="templ_in", default=str(uuid.uuid4()))
    mask_in = StringProperty(name="templ_in", default=str(uuid.uuid4()))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()))
    result_out = StringProperty(name="result_out", default=str(uuid.uuid4()))

    def get_anchor(self):
        return self.get("anchor_in", (-1, -1))

    method_in = EnumProperty(items=TEMPLATE_MATCH_MODE_ITEMS, default='TM_CCOEFF_NORMED', update=updateNode,
        description="Parameter specifying the comparison method, see cv::TemplateMatchModes.")

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
