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
import bpy
import cv2
import numpy as np
from bpy.types import Header, Menu
from bpy.types import INFO_HT_header as INFO_HT_header_old
from bpy.types import NODE_HT_header as NODE_HT_header_old
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

INFO_HT_header_old = INFO_HT_header_old

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


        layout.separator()

        # Snap
        row = layout.row(align=True)
        row.prop(toolsettings, "use_snap", text="")
        row.prop(toolsettings, "snap_node_element", text="", icon_only=True)
        if toolsettings.snap_node_element != 'INCREMENT':
            row.prop(toolsettings, "snap_target", text="")

        # row = layout.row(align=True)
        # row.operator("node.clipboard_copy", text="", icon='COPYDOWN')
        # row.operator("node.clipboard_paste", text="", icon='PASTEDOWN')

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
            sub.menu("INFO_MT_file")
            sub.menu("INFO_MT_window")
            sub.menu("INFO_MT_help")

        if window.screen.show_fullscreen:
            # layout.operator("screen.back_to_previous", icon='SCREEN_BACK', text="Back to Previous")
            layout.operator("screen.escape_full_screen", icon='SCREEN_BACK', text="Back to Previous")
            layout.separator()

        layout.separator()


        layout.separator()

        layout.template_running_jobs()

        layout.template_reports_banner()

        row = layout.row(align=True)
        row.operator("wm.splash", text="", icon='BLENDER', emboss=False)
        row.label(text=cv_lab_info(scene=scene))

        # XXX: BEFORE RELEASE, MOVE FILE MENU OUT OF INFO!!!
        """
        sinfo = context.space_data
        row = layout.row(align=True)
        row.prop(sinfo, "show_report_debug", text="Debug")
        row.prop(sinfo, "show_report_info", text="Info")
        row.prop(sinfo, "show_report_operator", text="Operators")
        row.prop(sinfo, "show_report_warning", text="Warnings")
        row.prop(sinfo, "show_report_error", text="Errors")

        row = layout.row()
        row.enabled = sinfo.show_report_operator
        row.operator("info.report_replay")

        row.menu("INFO_MT_report")
        """

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

    INFO_HT_header_old,
    # NODE_HT_header_old,
]
classes = [
    INFO_HT_header_new,
    # NODE_HT_header_new,
    ]


def register():
    unregister(classes_to_unregister)
    for class_ in classes:
        bpy.utils.register_class(class_)


def unregister(classes=classes):
    for class_ in reversed(classes):
        try:
            bpy.utils.unregister_class(class_)
        except:
            pass