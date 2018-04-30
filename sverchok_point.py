import inspect
import os
import importlib
from logging import getLogger
from collections import OrderedDict, defaultdict
from os.path import dirname, basename

import bpy
import sverchok
from . import nodes as ocvl_nodes
from .auth import ocvl_auth, auth_make_node_cats_new
from bpy.types import Addon, AddonPreferences, Addons

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import node_id
from sverchok.ui import nodeview_bgl_viewer_draw_mk2
from sverchok.utils.context_managers import sv_preferences


utils_needs = SverchCustomTreeNode, node_id, nodeview_bgl_viewer_draw_mk2, sv_preferences
logger = getLogger(__name__)


class MockSverchokAddonPreferences(AddonPreferences):
    bl_idname = "sverchok"

    selected_tab = "General"
    show_debug = False
    no_data_color = (1, 0.3, 0)
    exception_color = (0.8, 0.0, 0)
    heat_map = False
    heat_map_cold = (1, 1, 1)
    profile_mode = "NONE"
    developer_mode = False

    sv_theme = "default_theme"
    auto_apply_theme = False
    apply_theme_on_open = False
    color_viz = (1, 0.3, 0)
    color_tex = (0.5, 0.5, 1)
    color_sce = (0, 0.5, 0.2)
    color_lay = (0.674, 0.242, 0.363)
    color_gen = (0, 0.5, 0.5)
    frame_change_mode = "POST"
    show_icons = False
    over_sized_buttons = False
    enable_live_objin = False
    stethoscope_view_scale = 1.0
    stethoscope_view_xy_multiplier = 1.0
    defaults_location = ""
    external_editor = ""
    real_sverchok_path = ""

    log_level = "INFO"
    log_to_buffer = True
    log_to_buffer_clean = False
    log_to_file = False
    log_to_console = True
    log_buffer_name = "sverchok.log"
    log_file_name = ""


make_node_cats_new= auth_make_node_cats_new


def automatic_collection_new(directory):
    ignore_list = {}
    ignore_list['analyzer'] = ['bvh_raycast', 'bvh_nearest']
    ignore_list['scene'] = ['create_bvh_tree']

    nodes_dict = defaultdict(list)
    for subdir, dirs, files in os.walk(directory):
        current_dir = basename(subdir)
        if current_dir == '__pycache__':
            continue
        for file in files:
            if file == '__init__.py':
                continue
            if not file.endswith('.py'):
                continue
            nodes_dict[current_dir].append(file[:-3])

    # remove items found in ignore_list
    for k, v in ignore_list.items():
        items = nodes_dict.get(k)
        if items:
            for filename in v:
                try:
                    items.remove(filename)
                except:
                    logger.warning('Failed to remove {} from {} : check your spelling'.format(filename, k))

    # may not be used, but can be.
    return nodes_dict


def make_node_list_new(nodes=None, *args):
    node_list = []
    base_name = "sverchok.nodes"
    if nodes:
        for category, names in nodes.nodes_dict.items():
            importlib.import_module('.{}'.format(category), base_name)
            for name in names:
                im = importlib.import_module('.{}'.format(name), '{}.{}'.format(base_name, category))
                node_list.append(im)

    base_name = "ocvl.nodes"
    importlib.import_module(".nodes", "ocvl")
    for category, names in automatic_collection_new(os.path.join(dirname(__file__), "nodes")).items():
        importlib.import_module('.{}'.format(category), base_name)
        for name in names:
            im = importlib.import_module('.{}'.format(name), '{}.{}'.format(base_name, category))
            node_list.append(im)

    return node_list


def auto_gather_node_classes_new():
    """
    this produces a dict with mapping from bl_idname to class reference at runtime
    f.ex
          node_classes = {SvBMeshViewerMk2: <class svechok.nodes.viz ......> , .... }
    """

    node_cats = inspect.getmembers(sverchok.nodes, inspect.ismodule)
    for catname, nodecat in node_cats:
        node_files = inspect.getmembers(nodecat, inspect.ismodule)
        for filename, fileref in node_files:
            classes = inspect.getmembers(fileref, inspect.isclass)
            for clsname, cls in classes:
                try:
                    if cls.bl_rna.base.name == "Node":
                        sverchok.utils.node_classes[cls.bl_idname] = cls
                except:
                    ...

    node_cats = inspect.getmembers(ocvl_nodes, inspect.ismodule)
    for catname, nodecat in node_cats:
        node_files = inspect.getmembers(nodecat, inspect.ismodule)
        for filename, fileref in node_files:
            classes = inspect.getmembers(fileref, inspect.isclass)
            for clsname, cls in classes:
                logger.debug("Gather class: {}".format(clsname, cls))
                try:
                    if cls.bl_rna.base.name == "Node":
                        sverchok.utils.node_classes[cls.bl_idname] = cls
                except:
                    ...


def soft_reload_menu():
    """
    Function to reloading menu with nodes by COMM nad PRO versions.

    :return:
    """
    sverchok.core.root_modules = ["node_tree", "data_structure",  "ui", "nodes", "old_nodes", "sockets"]  # "menu", "core", "utils",
    sverchok.menu.make_node_cats = make_node_cats_new
    sverchok.core.make_node_list = make_node_list_new
    sverchok.utils.auto_gather_node_classes = auto_gather_node_classes_new
    from sverchok.menu import reload_menu
    reload_menu()


def reload_ocvl_nodes_classes():
    import ocvl.extend
    EXTENDED_NODE_PATH = getattr(ocvl.extend, "EXTENDED_NODE_PATH", "")
    EXTENDED_NODE_FILES = getattr(ocvl.extend, "EXTENDED_NODE_FILES", "")
    for node_file in EXTENDED_NODE_FILES:
        node_module = importlib.import_module("{}.{}".format(EXTENDED_NODE_PATH, node_file))
        importlib.reload(node_module)
        logger.info("Reload OCVL class: {}".format(node_module))


def reload_sverchok_addon():
    sverchok.core.root_modules = ["node_tree", "data_structure",  "ui", "nodes", "old_nodes", "sockets"]  # "menu", "core", "utils",
    sverchok.menu.make_node_cats = make_node_cats_new
    sverchok.core.make_node_list = make_node_list_new
    sverchok.utils.auto_gather_node_classes = auto_gather_node_classes_new

    sverchok_addon = bpy.context.user_preferences.addons.get("sverchok")
    if sverchok_addon:
        Addons.remove(sverchok_addon)
    sverchok_addon = Addons.new()
    sverchok_addon.module = "sverchok"
    if hasattr(bpy.context, "scene"):
        bpy.ops.wm.addon_disable(module=sverchok_addon.module)
        bpy.ops.wm.addon_enable(module=sverchok_addon.module)
    else:
        logger.info("Skip disable/enable {}".format(sverchok_addon.module))
        reload_ocvl_nodes_classes()


def reload_ocvl_addon():
    ocvl_addon = bpy.context.user_preferences.addons.get("ocvl")
    if ocvl_addon:
        Addons.remove(ocvl_addon)
    ocvl_addon = Addons.new()
    ocvl_addon.module = "ocvl"
    if hasattr(bpy.context, "scene"):
        bpy.ops.wm.addon_disable(module=ocvl_addon.module)
        bpy.ops.wm.addon_enable(module=ocvl_addon.module)
    else:
        logger.info("Skip disable/enable {}".format(ocvl_addon.module))


def reload_addons():
    reload_sverchok_addon()
    reload_ocvl_addon()
