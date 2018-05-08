import cv2
import os
import uuid
from logging import getLogger
from bpy.props import BoolProperty, StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode, updateNode

logger = getLogger(__name__)

current_path = os.path.abspath(__file__)
tutorial_path = os.path.join(current_path, "../../../tutorials")
full_tutorial_path = os.path.abspath(os.path.join(tutorial_path, "arithmetic_operations_on_images/arithmetic_operations_on_images.html"))


class OCVLDocsNode(OCVLPreviewNode):
    origin = StringProperty("")
    docs = BoolProperty(default=False)

    def sv_init(self, context):
        self.width = 180
        self.outputs.new("StringsSocket", "docs")

    def wrapped_process(self):
        pass

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.operator('wm.url_open', text="OCVL Web Panel".format(self.bl_label),icon='URL').url = 'https://ocvl-cms.herokuapp.com/admin/login/'
        col.operator('wm.url_open', text="OCVL Blog".format(self.bl_label),icon='URL').url = 'http://kube.pl/'
        col.operator('wm.url_open', text="OCVL Documentation".format(self.bl_label),icon='HELP').url = 'http://opencv-laboratory.readthedocs.io/en/latest/?badge=latest'
        col.operator('wm.url_open', text="OpenCV Documentation".format(self.bl_label),icon='HELP').url = 'https://docs.opencv.org/3.0-beta/index.html'
        col.operator('wm.url_open', text="Blender Documentation".format(self.bl_label),icon='HELP').url = 'https://docs.blender.org/manual/en/dev/editors/node_editor/introduction.html'
        col = layout.column(align=True)
        col.operator('node.tutorial_mode', text="Arithmetic Operations on Images",
                     icon='RENDERLAYERS').loc_tutorial_path = full_tutorial_path


def register():
    cv_register_class(OCVLDocsNode)


def unregister():
    cv_unregister_class(OCVLDocsNode)
