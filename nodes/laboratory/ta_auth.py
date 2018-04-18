from logging import getLogger
from bpy.props import BoolProperty, StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode, updateNode

logger = getLogger(__name__)


class OCVLAuthNode(OCVLPreviewNode):
    origin = StringProperty("")
    auth = BoolProperty(default=False)

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "auth")

    def wrapped_process(self):
        pass

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLAuthNode)


def unregister():
    cv_unregister_class(OCVLAuthNode)
