import cv2
import os
import uuid
from logging import getLogger
from bpy.props import BoolProperty, StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode, updateNode

logger = getLogger(__name__)


class OCVLHistoryNode(OCVLPreviewNode):
    origin = StringProperty("")
    history = BoolProperty(default=False)

    def sv_init(self, context):
        self.outputs.new("StringsSocket", "history")

    def wrapped_process(self):
        pass

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.operator('wm.recover_last_session', text='Recover last session', icon="RECOVER_LAST")



def register():
    cv_register_class(OCVLHistoryNode)


def unregister():
    cv_unregister_class(OCVLHistoryNode)
