import logging

import bpy
from ocvl.core.exceptions import NoDataError
from ocvl.core.image_utils import convert_to_gl_image
from ocvl.core.scene_utils import filter_areas
from ocvl.core.register_utils import ocvl_register, ocvl_unregister

logger = logging.getLogger(__name__)
TUTORIAL_HEARTBEAT_INTERVAL_RTSP_REFRESH = 2


class OCVLImageFullScreenOperator(bpy.types.Operator):
    bl_idname = "image.image_full_screen"
    bl_label = "OCVL Image Full Screen"

    origin: bpy.props.StringProperty("")

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
        if context.window.screen.show_fullscreen:
            bpy.ops.screen.back_to_previous()
        bpy.context.area.type = "NODE_EDITOR"
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
            except NoDataError as e:
                return {'CANCELLED'}
            bl_img = self._load_np_img_to_blender_data_image(img_name, img_data)
        else:
            return {'CANCELLED'}

        context.window_manager.modal_handler_add(self)
        bpy.context.area.type = "IMAGE_EDITOR"
        for area in filter_areas(bpy.context, area_type='IMAGE_EDITOR'):
            area.spaces.active.image = bl_img
        bpy.context.area.type = "IMAGE_EDITOR"
        bpy.ops.image.view_all(fit_view=True)
        bpy.ops.screen.screen_full_area()

        args = (self, context)

        return {'RUNNING_MODAL'}


class OCVLImageImporterOperator(bpy.types.Operator):
    bl_idname = "image.ocvl_image_importer"
    bl_label = "Open Image"
    bl_options = {'REGISTER'}

    filter_glob: bpy.props.StringProperty(default="*.tif;*.png;*.jpeg;*.jpg", options={'HIDDEN'})


    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for importing the font file",
        maxlen=1024, default="", subtype='FILE_PATH'
    )

    origin: bpy.props.StringProperty("")

    def execute(self, context):
        node_tree, node_name = self.origin.split('|><|')
        node = bpy.data.node_groups[node_tree].nodes[node_name]
        node.loc_filepath = self.filepath
        node.loc_name_image = ''
        node.process()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


def register():
    ocvl_register(OCVLImageFullScreenOperator)
    ocvl_register(OCVLImageImporterOperator)


def unregister():
    ocvl_unregister(OCVLImageImporterOperator)
    ocvl_unregister(OCVLImageFullScreenOperator)
