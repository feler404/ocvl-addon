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
        self.width = 180
        self.outputs.new("StringsSocket", "history")

    def wrapped_process(self):
        pass

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.operator('wm.recover_last_session', text='Recover last session', icon="RECOVER_LAST")
        row = layout.row()
        col = row.column()
        col_split = col.split(0.5, align=True)
        col_split.operator('node.change_theme_light', text='Light', icon="OUTLINER_OB_LAMP")
        col_split.operator('node.change_theme_dark', text='Dark', icon="OUTLINER_DATA_LAMP")
        row = layout.row()
        col = row.column()
        col.operator('node.tutorial_mode', text="Tutorial - First steps", icon='PARTICLES')

def register():
    cv_register_class(OCVLHistoryNode)


def unregister():
    cv_unregister_class(OCVLHistoryNode)
