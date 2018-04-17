import cv2
import os
import uuid
from bpy.props import BoolProperty, StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode, updateNode


class OCVLHelloNode(OCVLPreviewNode):
    origin = StringProperty("")
    image_out = StringProperty(default=str(uuid.uuid4()))
    login_in = StringProperty(name="Login", default="", description="Login", maxlen=60)
    password_in = StringProperty(name="Password", default="", subtype="PASSWORD", description="Password", maxlen=60)
    is_licence_key = BoolProperty(name="Licence Key", default=False, update=updateNode)
    licence_key_in = StringProperty(name="Licence Key", default="", description="licence_key_in", maxlen=600)

    origin = StringProperty("")

    def sv_init(self, context):
        self.width = 512
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        baner_dir = os.path.abspath(os.path.join(current_dir, "../../datafiles/"))
        loc_filepath = os.path.join(baner_dir, "ocvl_baner.png")
        image = cv2.imread(loc_filepath)
        uuid_ = None
        image, self.image_out = self._update_node_cache(image=image, resize=False, uuid_=uuid_)

        self.make_textures(image, uuid_=self.image_out, width=512, height=288)
        print(111111111)

    def wrapped_process(self):
        print(999999999999)

    def _update_node_cache(self, image=None, resize=False, uuid_=None):
        old_image_out = self.image_out
        self.socket_data_cache.pop(old_image_out, None)
        uuid_ = uuid_ if uuid_ else str(uuid.uuid4())
        self.socket_data_cache[uuid_] = image
        print(222222222)
        return image, uuid_

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.operator('wm.splash', text='', icon="FULLSCREEN")
        self.draw_preview(layout=layout, prop_name="image_out", location_x=10, location_y=40)
        self.add_button(layout, "is_licence_key")


        if not self.is_licence_key:
            row = layout.row()
            row.prop(self, "login_in", "Login")
            row = layout.row()
            row.prop(self, "password_in", "Password")
        else:
            row = layout.row()
            row.prop(self, "licence_key_in", "Licence Key")



def register():
    cv_register_class(OCVLHelloNode)


def unregister():
    cv_unregister_class(OCVLHelloNode)
