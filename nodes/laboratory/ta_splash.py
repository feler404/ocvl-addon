import cv2
import os
import uuid
from logging import getLogger
from bpy.props import BoolProperty, StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode
from ...auth import ocvl_auth

logger = getLogger(__name__)


class OCVLSplashNode(OCVLPreviewNode):
    origin = StringProperty("")
    image_out = StringProperty(default=str(uuid.uuid4()))

    login_in = StringProperty(name="Login", default="", description="Login", maxlen=60)
    password_in = StringProperty(name="Password", default="", subtype="PASSWORD", description="Password", maxlen=60)
    is_remember_in = BoolProperty(name="Remember", default=True, description="Remember credentials")

    is_licence_key = BoolProperty(name="Licence Key", default=False)
    licence_key_in = StringProperty(name="Licence Key", default="", description="licence_key_in", maxlen=600)

    auth = BoolProperty(name="Auth", default=False)
    docs = BoolProperty(default=False)
    history = BoolProperty(default=False)

    is_splash_loaded = BoolProperty(default=False)

    def sv_init(self, context):
        self.width = 512
        self.use_custom_color = True
        self.color = (0, 0, 0)
        self.outputs.new("StringsSocket", "auth")
        self.inputs.new("StringsSocket", "history")
        self.inputs.new("StringsSocket", "docs")

    def wrapped_process(self):
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        baner_dir = os.path.abspath(os.path.join(current_dir, "../../datafiles/"))
        loc_filepath = os.path.join(baner_dir, "ocvl_baner.png")
        image = cv2.imread(loc_filepath)
        image, self.image_out = self._update_node_cache(image=image, resize=False)
        self.make_textures(image, uuid_=self.image_out, width=512, height=288)

    def _update_node_cache(self, image=None, resize=False, uuid_=None):
        old_image_out = self.image_out
        self.socket_data_cache.pop(old_image_out, None)
        uuid_ = uuid_ if uuid_ else str(uuid.uuid4())
        self.socket_data_cache[uuid_] = image
        return image, uuid_

    def draw_buttons(self, context, layout):
        self.draw_preview(layout=layout, prop_name="image_out", location_x=10, location_y=50)
        if ocvl_auth.ocvl_version is ocvl_auth.COMMUNITY_VERSION:
            self.layout_for_community_version(context, layout)
        if ocvl_auth.ocvl_version is ocvl_auth.PRO_VERSION:
            self.layout_for_pro_version(context, layout)

    def layout_for_community_version(self, context, layout):
        pass

    def layout_for_pro_version(self, context, layout):
        if ocvl_auth.ocvl_pro_version_auth:
            row = layout.row()
            row.operator('node.clean_desk', text="Start with blank desk", icon='FILE_TICK')
            row.operator('wm.recover_last_session', text='Recover last session', icon="RECOVER_LAST")
            row.operator('wm.url_open', text="Store".format(self.bl_label), icon='MOD_CLOTH').url = 'http://kube.pl/'
            row = layout.row()
            col = row.column()
            col_split = col.split(0.5, align=True)
            col_split.operator('wm.url_open', text="First step".format(self.bl_label), icon='PARTICLE_DATA').url = 'http://kube.pl/'
            col_split.operator('wm.url_open', text="Tutorial 1".format(self.bl_label), icon='URL').url = 'http://kube.pl/'
            col_split = col.split(0.5, align=True)
            col_split.operator('wm.url_open', text="Tutorial 2".format(self.bl_label), icon='URL').url = 'http://kube.pl/'
            col_split.operator('wm.url_open', text="Tutorial 3".format(self.bl_label), icon='URL').url = 'http://kube.pl/'
        else:
            col = layout.column(align=True)

            self.add_button(layout, "is_licence_key")

            if not self.is_licence_key:
                row = layout.row()
                row.prop(self, "login_in", "Login")
                row.prop(self, "password_in", "Password")
                row.prop(self, "is_remember_in", "Remember")
                get_args = "?login={}&password={}".format(self.login_in, self.password_in)
                get_fn_url = 'login'
            else:
                row = layout.row()
                row.prop(self, "licence_key_in", "Licence Key")
                get_args = "?licence_key={}".format(self.licence_key_in)
                get_fn_url = 'licence'
            row = layout.row()
            row.operator('node.requests_splash', text='Submit', icon='FILE_TICK').origin = self.get_node_origin(props_name=[get_fn_url, get_args])


def register():
    cv_register_class(OCVLSplashNode)


def unregister():
    cv_unregister_class(OCVLSplashNode)
