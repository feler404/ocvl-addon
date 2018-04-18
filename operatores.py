import bpy
import logging
import urllib.parse
from bpy.props import StringProperty
from pynput.keyboard import Key, Controller

from .nodes.laboratory.ta_auth import AUTH_NODE_NAME
from .utils import convert_to_gl_image, cv_register_class, cv_unregister_class
from sverchok.core.socket_data import SvNoDataError
import requests

from .auth import ocvl_auth, auth_pro_confirm, auth_pro_reject

logger = logging.getLogger(__name__)

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


class OCVLShowTextInTextEditorOperator(bpy.types.Operator):
    bl_idname = "text.show_help_in_text_editor"
    bl_label = "OCVL show help in text editor"

    origin = StringProperty("")

    def modal(self, context, event):

        if event.type in {'ESC'}:

            bpy.context.area.type = "NODE_EDITOR"
            if context.window.screen.show_fullscreen:
                bpy.ops.screen.back_to_previous()
            if 'TEXT_INPUT_NODE' in bpy.data.texts.keys():
                bpy.data.texts.remove(bpy.data.texts["TEXT_INPUT_NODE"])
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        bpy.context.area.type = "TEXT_EDITOR"
        node_tree, node_name, *props_name = self.origin.split('|><|')
        self.node = bpy.data.node_groups[node_tree].nodes[node_name]

        if node_name not in bpy.data.texts.keys():
            bpy.data.texts.new(node_name)
            text = bpy.data.texts[node_name]
            doc = getattr(self.node, '__doc__', None) or 'Lack of offline documentation.'
            text.write(doc)

        self.text = context.space_data.text = bpy.data.texts[node_name]
        context.space_data.show_line_numbers = True
        context.space_data.show_word_wrap = True
        context.space_data.show_syntax_highlight = True
        context.space_data.font_size = 16
        bpy.ops.screen.screen_full_area()

        return {'RUNNING_MODAL'}


class OCVLClearDeskOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.clean_desk"
    bl_label = "Clean Desk"

    def execute(self, context):
        for node_group in bpy.data.node_groups:
            for node in node_group.nodes:
                node.select = True
        bpy.ops.node.delete()
        return {'FINISHED'}


class OCVLRequestsSplashOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.requests_splash"
    bl_label = "Requests Splash"

    origin = StringProperty("")

    def invoke(self, context, event):
        node_tree, node_name, fn_name, fn_args = self.origin.split('|><|')
        node = bpy.data.node_groups[node_tree].nodes[node_name]
        url = "{}{}{}".format(ocvl_auth.OCVL_PANEL_URL, fn_name, fn_args)
        response = requests.get(url=url)
        auth_node = self._get_auth_node(node_tree, node)
        if response.status_code == 200:
            auth_pro_confirm(node, url, response)
        else:
            auth_pro_reject(node, url, response)
        auth_node["status_code"] = response.status_code
        auth_node["response_content"] = response.content

        logger.info("Request: {}".format(url))
        logger.info("Response: {}, payload: {}".format(response, response.content))

        print(node_tree, node_name, fn_name, fn_args)

        return {'FINISHED'}

    @staticmethod
    def _get_auth_node(node_tree, fall_back):
        for link in bpy.data.node_groups[node_tree].links:
            if link.to_node.name == AUTH_NODE_NAME:
                return link.to_node
        return fall_back


def register():
    cv_register_class(OCVLImageFullScreenOperator)
    cv_register_class(EscapeFullScreenOperator)
    cv_register_class(OCVLShowTextInTextEditorOperator)
    cv_register_class(OCVLClearDeskOperator)
    cv_register_class(OCVLRequestsSplashOperator)


def unregister():
    cv_unregister_class(OCVLRequestsSplashOperator)
    cv_unregister_class(OCVLClearDeskOperator)
    cv_unregister_class(OCVLShowTextInTextEditorOperator)
    cv_unregister_class(EscapeFullScreenOperator)
    cv_unregister_class(OCVLImageFullScreenOperator)
