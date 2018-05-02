# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>
import webbrowser

import bpy
import cv2
import numpy as np
from bpy.types import Header, Menu
from bpy.types import INFO_HT_header as INFO_HT_header_old
from bpy.types import NODE_HT_header as NODE_HT_header_old
from bpy.types import INFO_MT_file as INFO_MT_file_old
from bpy.types import INFO_MT_help as INFO_MT_help_old
from bpy.types import (
NODE_PT_grease_pencil,
NODE_PT_tools_grease_pencil_brush,
NODE_PT_tools_grease_pencil_edit,
IMAGE_PT_tools_grease_pencil_sculpt,
NODE_PT_tools_grease_pencil_brushcurves,
NODE_PT_grease_pencil_tools,
NODE_PT_tools_grease_pencil_draw,
NODE_PT_grease_pencil_palettecolor,
NODE_PT_tools_grease_pencil_sculpt,

IMAGE_PT_grease_pencil,
IMAGE_PT_game_properties,
IMAGE_PT_grease_pencil_palettecolor,
IMAGE_PT_tools_grease_pencil_brush,
IMAGE_PT_tools_grease_pencil_edit,
IMAGE_PT_tools_grease_pencil_brushcurves,
IMAGE_PT_tools_grease_pencil_sculpt,
IMAGE_PT_tools_grease_pencil_draw,

TEXT_MT_templates,

)

from .auth import ocvl_auth



class NODE_HT_header_new(Header):
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        ob = context.object
        snode = context.space_data
        snode_id = snode.id
        id_from = snode.id_from
        toolsettings = context.tool_settings

        row = layout.row(align=True)
        row.label(icon='NODETREE')
        # row.template_header()

        if context.area.show_menus:
            row.menu("NODE_MT_view")
            row.menu("NODE_MT_select")
            row.menu("NODE_MT_add")
            row.menu("NODE_MT_node")

        layout.template_ID(snode, "node_tree", new="node.new_node_tree")

        layout.prop(snode, "pin", text="")
        layout.operator("node.tree_path_parent", text="", icon='FILE_PARENT')

        layout.separator()

        # Auto-offset nodes (called "insert_offset" in code)
        layout.prop(snode, "use_insert_offset", text="")

        # Snap
        row = layout.row(align=True)
        row.prop(toolsettings, "use_snap", text="")
        row.prop(toolsettings, "snap_node_element", icon_only=True)
        if toolsettings.snap_node_element != 'GRID':
            row.prop(toolsettings, "snap_target", text="")

        row = layout.row(align=True)
        row.operator("node.clipboard_copy", text="", icon='COPYDOWN')
        row.operator("node.clipboard_paste", text="", icon='PASTEDOWN')

        layout.template_running_jobs()


class INFO_HT_header_new(Header):
    bl_space_type = 'INFO'

    def draw(self, context):
        layout = self.layout

        window = context.window
        scene = context.scene
        rd = scene.render

        row = layout.row(align=True)
        row.label(icon='INFO')
        # row.template_header()

        if context.area.show_menus:
            sub = row.row(align=True)
            sub.menu("INFO_MT_file_new")
            sub.menu("INFO_MT_window")
            sub.menu("INFO_MT_help_new")

        if window.screen.show_fullscreen:
            # layout.operator("screen.back_to_previous", icon='SCREEN_BACK', text="Back to Previous")
            layout.operator("screen.escape_full_screen", icon='SCREEN_BACK', text="Back to Previous")
            layout.separator()

        layout.separator()


        layout.separator()

        layout.template_running_jobs()

        layout.template_reports_banner()

        row = layout.row(align=True)
        row.operator("node.show_node_splash", text="", icon='COLOR', emboss=False)
        row.label(text=cv_lab_info(scene=scene))


class INFO_MT_file_new(Menu):
    bl_label = "File"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.read_homefile", text="New", icon='NEW')
        layout.operator("wm.open_mainfile", text="Open...", icon='FILE_FOLDER')
        layout.menu("INFO_MT_file_open_recent", icon='OPEN_RECENT')
        layout.operator("wm.revert_mainfile", icon='FILE_REFRESH')
        layout.operator("wm.recover_last_session", icon='RECOVER_LAST')
        layout.operator("wm.recover_auto_save", text="Recover Auto Save...", icon='RECOVER_AUTO')

        layout.separator()

        layout.operator_context = 'EXEC_AREA' if context.blend_data.is_saved else 'INVOKE_AREA'
        layout.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save As...", icon='SAVE_AS')
        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save Copy...", icon='SAVE_COPY').copy = True

        layout.separator()

        layout.operator_context = 'EXEC_AREA'
        if bpy.data.is_dirty and context.user_preferences.view.use_quit_dialog:
            layout.operator_context = 'INVOKE_SCREEN'  # quit dialog
        layout.operator("wm.quit_blender", text="Quit", icon='QUIT')


class INFO_MT_help_new(Menu):
    bl_label = "Help"

    def draw(self, context):
        layout = self.layout

        layout.operator(
                "wm.url_open", text="OCVL Documentation", icon='HELP',
                ).url = "http://opencv-laboratory.readthedocs.io/en/latest/?badge=latest"
        layout.operator(
                "wm.url_open", text="OpenCV Documentation", icon='HELP',
                ).url = "https://docs.opencv.org/3.0-beta/index.html"
        layout.operator(
                "wm.url_open", text="Blender Documentation", icon='HELP',
                ).url = "https://docs.blender.org/manual/en/dev/editors/node_editor/introduction.html"
        layout.separator()

        layout.operator(
                "wm.url_open", text="OCVL Web Panel", icon='URL',
                ).url = "https://ocvl-cms.herokuapp.com/admin/login/"
        layout.operator(
                "wm.url_open", text="OCVL Blog", icon='URL',
                ).url = "http://kube.pl/"

        layout.separator()

        layout.operator("node.show_node_splash", icon='COLOR')
# https://github.com/trevortomesh/Blender-Python-Learning-Environment/blob/master/BPyLE/lin/blenderPyLE-2.64a-linux64/2.64/scripts/startup/bl_ui/space_info.py


def cv_lab_info(scene):
    cv_version = "CV:{}".format(cv2.__version__)
    np_version = "NumPy:{}".format(np.version.full_version)

    images_number = len(bpy.data.images)
    imgs_total_size = 0
    for img in bpy.data.images:
        imgs_total_size += img.size[0] * img.size[1] * img.depth

    imgs_total_size = "Img:{0:.2f}MB".format(imgs_total_size/(8*1024*1024))

    original_statistics = scene.statistics().split("|")
    blender_version = bpy.app.version
    blender_version_2 = original_statistics[0]
    blender_memory = original_statistics[6]

    node_number = 0
    for node_group in bpy.data.node_groups.values():
        node_number += len(node_group.nodes)
    node_number = "Nodes:{}".format(node_number)
    return "|".join([blender_version_2, cv_version, np_version, imgs_total_size, node_number, blender_memory])


class SvViewHelpForNodeNew(bpy.types.Operator):
    from bpy.props import StringProperty
    bl_idname = "node.view_node_help"
    bl_label = "display a browser with compiled html"
    kind = StringProperty(default='online')

    def execute(self, context):
        return {'FINISHED'}


class SvViewHelpForNodeNew(bpy.types.Operator):
    from bpy.props import StringProperty
    bl_idname = "node.view_node_help"
    bl_label = "display a browser with compiled html"
    kind = StringProperty(default='online')

    def execute(self, context):
        active_node = context.active_node

        if self.kind == 'online':
            url = 'https://docs.opencv.org/3.0-last-rst/search.html?q={}&check_keywords=yes&area=default'.format(active_node.bl_label)
            webbrowser.open(url)
        elif self.kind == 'offline':
            self.report({'INFO'}, 'Documentation docstring - {}'.format(active_node.bl_label))
        elif self.kind == 'github':
            webbrowser.open("https://github.com/feler404/ocvl-addon")

        return {'FINISHED'}


class SvViewSourceForNodeNew(bpy.types.Operator):
    from bpy.props import StringProperty
    bl_idname = "node.sv_view_node_source"
    bl_label = "display the source in your editor"
    kind = StringProperty(default='external')

    def execute(self, context):
        webbrowser.open("https://github.com/feler404/ocvl-addon")
        return {'FINISHED'}


sv_tree_types = {'SverchCustomTreeType', 'SverchGroupTreeType'}

class NODEVIEW_MT_Dynamic_Menu_new(bpy.types.Menu):
    bl_label = "Sverchok Nodes"

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        if tree_type in sv_tree_types:
            return True

    def draw(self, context):

        tree_type = context.space_data.tree_type
        if not tree_type in sv_tree_types:
            return

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        if self.bl_idname == 'NODEVIEW_MT_Dynamic_Menu_new':
            layout.operator("node.sv_extra_search", text="Search", icon='OUTLINER_DATA_FONT')


        layout.separator()
        layout.menu("NODE_MT_category_SVERCHOK_GROUPS", icon="RNA")



def valid_active_node(nodes):
    if nodes:
        # a previously active node can remain active even when no nodes are selected.
        if nodes.active and nodes.active.select:
            return nodes.active


def has_outputs(node):
    return node and len(node.outputs)


class SvNodeviewRClickMenu_new(bpy.types.Menu):
    bl_label = "Right click menu"
    bl_idname = "NODEVIEW_MT_sv_rclick_menu"

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        return tree_type in sv_tree_types

    def draw(self, context):
        layout = self.layout
        tree = context.space_data.edit_tree
        nodes = tree.nodes
        node = valid_active_node(nodes)

        if node:
            if has_outputs(node):
                layout.operator("node.sv_deligate_operator", text="Connect Viewer").fn = "Viewer"

            if hasattr(node, "rclick_menu"):
                node.rclick_menu(context, layout)

        else:
            layout.menu("NODEVIEW_MT_Dynamic_Menu_new", text='node menu')

        if node and len(node.outputs):
            layout.operator("node.sv_deligate_operator", text="Connect stethoscope").fn = "Stethoscope"


def add_connection_new(tree, bl_idname_new_node, offset):

    nodes = tree.nodes
    links = tree.links

    existing_node = nodes.active

    if isinstance(bl_idname_new_node, str):

        new_node = nodes.new(bl_idname_new_node)

        outputs = existing_node.outputs
        inputs = new_node.inputs

        links.new(outputs[0], inputs[0])


class SvGenericDeligationOperator_new(bpy.types.Operator):

    bl_idname = "node.sv_deligate_operator"
    bl_label = "Execute generic code"

    fn = bpy.props.StringProperty(default='')

    def execute(self, context):
        tree = context.space_data.edit_tree

        if self.fn == 'Viewer':
            add_connection_new(tree, bl_idname_new_node=ocvl_auth.viewer_name, offset=[220, 0])
        elif self.fn == 'Stethoscope':
            add_connection_new(tree, bl_idname_new_node="SvStethoscopeNodeMK2", offset=[220, 0])

        return {'FINISHED'}


classes_to_unregister = [
    NODE_PT_grease_pencil,
    NODE_PT_tools_grease_pencil_brush,
    NODE_PT_tools_grease_pencil_edit,
    NODE_PT_tools_grease_pencil_brushcurves,
    NODE_PT_grease_pencil_tools,
    NODE_PT_tools_grease_pencil_draw,
    NODE_PT_grease_pencil_palettecolor,
    NODE_PT_tools_grease_pencil_sculpt,

    IMAGE_PT_grease_pencil,
    IMAGE_PT_game_properties,
    IMAGE_PT_grease_pencil_palettecolor,
    IMAGE_PT_tools_grease_pencil_brush,
    IMAGE_PT_tools_grease_pencil_edit,
    IMAGE_PT_tools_grease_pencil_brushcurves,
    IMAGE_PT_tools_grease_pencil_sculpt,
    IMAGE_PT_tools_grease_pencil_draw,

    # TEXT_MT_templates,
    NODE_HT_header_old,
    INFO_HT_header_old,
    INFO_MT_file_old,
    INFO_MT_help_old,


]
classes = [
    NODE_HT_header_new,
    INFO_HT_header_new,
    INFO_MT_file_new,
    INFO_MT_help_new,
    SvViewHelpForNodeNew,
    SvViewSourceForNodeNew,
    NODEVIEW_MT_Dynamic_Menu_new,
    SvNodeviewRClickMenu_new,
    SvGenericDeligationOperator_new,

    ]


def remove_panels():
    for pt in bpy.types.Panel.__subclasses__():
        if pt.bl_space_type == 'NODE_EDITOR':
            if pt.__name__ in ["SvUserPresetsPanel", "SverchokToolsMenu", "SverchokIOLayoutsMenu", "SverchokToolsMenu",
                               "SvTestingPanel", "SverchokIOLayoutsMenu"]:
                bpy.utils.unregister_class(pt)



def register():
    unregister(classes_to_unregister)
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister(classes=classes):
    import bpy
    remove_panels()
    for class_ in reversed(classes):
        try:
            bpy.utils.unregister_class(class_)
        except:
            pass