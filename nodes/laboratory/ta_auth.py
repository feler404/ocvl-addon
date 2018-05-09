from logging import getLogger
from bpy.props import BoolProperty, StringProperty, IntProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode, updateNode
from ...auth import (
    ocvl_auth, ocvl_user, ANONYMOUS, OCVL_GITHUB_ISSUE_TEMPLATE, COMMUNITY_VERSION,
    OCVL_LINK_UPGRADE_PROGRAM_TO_PRO,
    OCVL_LINK_TO_OCVL_PANEL,
    OCVL_LINK_TO_CREATE_ACCOUNT)

logger = getLogger(__name__)


class OCVLAuthNode(OCVLPreviewNode):
    origin = StringProperty("")
    auth = BoolProperty(default=False)
    status_code = IntProperty(default=0)
    response_content = StringProperty(default="")

    def sv_init(self, context):
        self.width = 180
        self.inputs.new("StringsSocket", "auth")

    def wrapped_process(self):
        pass

    def draw_buttons(self, context, layout):
        name = ocvl_user.name
        msg = ""
        icon = 'QUESTION'
        if self.status_code == 0:
            icon = 'QUESTION'
            if ocvl_auth.ocvl_version == COMMUNITY_VERSION:
                col = layout.column(align=True)
                # col.operator('wm.url_open', text="Upgrade program to PRO".format(self.bl_label), icon='SOLO_ON').url = OCVL_LINK_UPGRADE_PROGRAM_TO_PRO
                col.operator('wm.url_open', text="Create account".format(self.bl_label), icon='INFO').url = OCVL_LINK_TO_CREATE_ACCOUNT
        elif self.status_code == 200:
            col = layout.column(align=True)
            col.operator('wm.url_open', text="OCVL Web Panel".format(self.bl_label),
                         icon='URL').url = OCVL_LINK_TO_OCVL_PANEL
            icon = 'FILE_TICK'
        elif self.status_code == 401:
            msg = "Incorrect credentials / Licence Key"
            icon = "ERROR"
        elif self.status_code >= 500:
            msg = "Server Error"
            icon = "ERROR"
            url = OCVL_GITHUB_ISSUE_TEMPLATE.format(title="OCVL web authenticate error 500", body=self.response_content)
            col = layout.column(align=True)
            col.operator('wm.url_open', text="Report a problem".format(self.bl_label), icon='URL').url = url
        else:
            url = OCVL_GITHUB_ISSUE_TEMPLATE.format(title="OCVL web authenticate unsupported error", body=self.response_content)
            col = layout.column(align=True)
            col.operator('wm.url_open', text="Report a problem".format(self.bl_label), icon='URL').url = url
            msg = "Unsupported error"
            icon = "ERROR"
        layout.label(msg)
        layout.label(name, icon=icon)


AUTH_NODE_NAME = OCVLAuthNode.__name__[4:-4]


def register():
    cv_register_class(OCVLAuthNode)


def unregister():
    cv_unregister_class(OCVLAuthNode)
