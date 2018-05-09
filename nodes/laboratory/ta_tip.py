import cv2
import os
import uuid
import bpy
from logging import getLogger
from bpy.props import BoolProperty, StringProperty, IntProperty

from .ta_first_step import show_long_tip, TIP_STEP_2
from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode

logger = getLogger(__name__)


class OCVLTipNode(OCVLPreviewNode):
    tip = IntProperty(default=0)
    image_out = StringProperty(default='')

    is_splash_loaded = BoolProperty(default=False)

    def sv_init(self, context):
        self.width = 512
        self.inputs.new("StringsSocket", "tip")

    def wrapped_process(self):
        if self.tip != bpy.tutorial_first_step:
            self.tip = bpy.tutorial_first_step
            current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
            baner_dir = os.path.abspath(os.path.join(current_dir, "../../tutorials/first_steps/"))
            loc_filepath = os.path.join(baner_dir, "step_{}.png".format(bpy.tutorial_first_step))
            image = cv2.imread(loc_filepath)
            self.make_textures(image, uuid_=self.image_out, width=1024, height=512)


    def _update_node_cache(self, image=None, resize=False, uuid_=None):
        old_image_out = self.image_out
        self.socket_data_cache.pop(old_image_out, None)
        uuid_ = uuid_ if uuid_ else str(uuid.uuid4())
        self.socket_data_cache[uuid_] = image
        return image, uuid_

    def draw_buttons(self, context, layout):
        self.draw_preview(layout=layout, prop_name="image_out", location_x=10, location_y=70, proportion=0.5)
        col = layout.column(align=True)
        show_long_tip("""afsdf asdf adsfoiuadsiufads iuf halsdjkfl askjdhfl akjsdhfl aksjdhfl adksjhfl askdjfl akdjs flakjdsf"
                      "alsdjfal sdkjf alsdkjf alsdkjf alsd asdf asldkjfhl adksjhfl aksdjhfl kajsdhfl akjsdl kj 
                       adflkajsdf lkajsdhfl kjadshfl kajsdhfl aksdjhlasdkjhlasfdjk""", col)


def register():
    cv_register_class(OCVLTipNode)


def unregister():
    cv_unregister_class(OCVLTipNode)
