import uuid
from bpy.props import BoolProperty, StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLHelloNode(OCVLNode):

    login_in = StringProperty(name="Login", default="", description="Login", maxlen=60)
    password_in = StringProperty(name="Password", default="", subtype="PASSWORD", description="Password", maxlen=60)

    is_licence_key = BoolProperty(name="Licence Key", default=False, update=updateNode)
    licence_key_in = StringProperty(name="Licence Key", default="", description="licence_key_in", maxlen=600)

    origin = StringProperty("")

    def sv_init(self, context):
        self.width = 400

    def wrapped_process(self):
        pass

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.operator('object.cv_open_splash_operator', text='', icon="FULLSCREEN").origin = self.get_node_origin()
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
