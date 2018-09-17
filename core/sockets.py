import bpy
from ocvl.core.register_utils import ocvl_register, ocvl_unregister


class OCVLUUIDSocket(bpy.types.NodeSocket):
    '''Renderman co-shader input/output'''
    bl_idname = 'OCVLUUIDSocket'
    bl_label = 'OCVLUUIDSocket'

    uuid = bpy.props.StringProperty(default="")

    # Optional function for drawing the socket input value
    def draw_value(self, context, layout, node):
        layout.label(self.name)

    def draw_color(self, context, node):
        return (0.1, 1.0, 0.2, 1)

    def draw(self, context, layout, node, text):
        layout.label(text)
        pass


def register():
    ocvl_register(OCVLUUIDSocket)


def unregister():
    ocvl_unregister(OCVLUUIDSocket)
