import bpy

from bpy.props import StringProperty
from pynput.keyboard import Key, Controller

from .utils import convert_to_gl_image
from sverchok.core.socket_data import SvNoDataError


class EscapeFullScreenOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "screen.escape_full_screen"
    bl_label = "Escape Full Screen Operator"

    def execute(self, context):
        keyboard = Controller()
        keyboard.press(Key.esc)
        bpy.ops.screen.back_to_previous()
        return {'FINISHED'}


class OCVLImageFullScreenOperator(bpy.types.Operator):
    bl_idname = "image.image_full_screen"
    bl_label = "OCVL Image Full Screen"

    origin = StringProperty("")

    def modal(self, context, event):
        if event.type in {'ESC'}:
            return self._exit(context, exit_mode='CANCELLED')

        return {'PASS_THROUGH'}

    def _load_np_img_to_blender_data_image(self, img_name, img_data):
        bl_img = bpy.data.images.get(img_name)
        if bl_img:
            return bl_img
        gl_img_data = convert_to_gl_image(img_data)
        height, width = img_data.shape[:2]
        bl_img = bpy.data.images.new(img_name, width, height)
        bl_img.pixels = list(gl_img_data.flat)
        return bl_img

    def _exit(self, context, exit_mode='FINISHED'):
        bpy.context.area.type = "NODE_EDITOR"
        if context.window.screen.show_fullscreen:
            bpy.ops.screen.back_to_previous()
        return {exit_mode}

    def invoke(self, context, event):
        self.points = []
        self.points = []
        node_tree, node_name, *props_name = self.origin.split('|><|')
        self.node = node = bpy.data.node_groups[node_tree].nodes[node_name]
        self.props_name = props_name
        self.props_counter = 0
        if node.inputs["image_in"].is_linked:

            try:
                img_data = node.get_from_props("image_in")
                img_name = node.inputs.get("image_in").sv_get()
            except SvNoDataError as e:
                return {'CANCELLED'}
            bl_img = self._load_np_img_to_blender_data_image(img_name, img_data)
        else:
            return {'CANCELLED'}

        context.window_manager.modal_handler_add(self)
        bpy.context.area.type = "IMAGE_EDITOR"
        for area in bpy.context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.spaces.active.image = bl_img
        bpy.context.area.type = "IMAGE_EDITOR"
        bpy.ops.image.view_all(fit_view=True)
        bpy.ops.screen.screen_full_area()

        args = (self, context)

        return {'RUNNING_MODAL'}





def register():
    bpy.utils.register_class(OCVLImageFullScreenOperator)
    bpy.utils.register_class(EscapeFullScreenOperator)


def unregister():
    bpy.utils.unregister_class(EscapeFullScreenOperator)
    bpy.utils.unregister_class(OCVLImageFullScreenOperator)
