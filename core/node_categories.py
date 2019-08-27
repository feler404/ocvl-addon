import logging
import os
from collections import defaultdict
from importlib import util

import bpy
import ocvl
from nodeitems_utils import NodeCategory, NodeItem, _node_categories, unregister_node_categories  # register_node_categories
from ocvl.core import settings
from ocvl.core.register_utils import register_node, unregister_node

logger = logging.getLogger(__name__)


CATEGORY_CONFIG_MAP = {}  # icon, name, description
BUILD_CATEGORIES = defaultdict(lambda: [])
SUBCATEGORY_SEPARATOR = "__"


def is_second_extension_path():
    ocvl_path = ocvl.__path__[0]
    ocvl_pro_path = os.path.join(os.path.sep.join(ocvl_path.split(os.path.sep)[:-1]), settings.OCVL_PRO_DIR_NAME)
    if os.path.exists(ocvl_pro_path):
        return True
    else:
        return False


class OCVLNodeCategory(NodeCategory):
    icon = None
    name = None
    description = None

    @classmethod
    def pull(cls, context):
        logger.info("Categories Node pull")
        return context.space_data.tree_type == settings.OCVL_NODE_TREE_TYPE


def is_node_class_name(class_name):
    return class_name.startswith(settings.PREFIX_NODE_CLASS) and \
           class_name.endswith(settings.SUFFIX_NODE_CLASS) and \
           class_name not in settings.BLACK_LIST_FOR_REGISTER_NODE


def register_node_categories(identifier, cat_list):
    # works as draw function for menus
    def draw_node_item(self, context):
        layout = self.layout
        col = layout.column()
        for item in self.category.items(context):
            item.draw(item, col, context)

    def draw_add_menu(self, context):
        layout = self.layout
        for cat in cat_list:
            if cat.poll(context):
                if not SUBCATEGORY_SEPARATOR in cat.identifier:
                    layout.menu("NODE_MT_category_%s" % cat.identifier, icon=cat.icon)

    if identifier in _node_categories:
        raise KeyError("Node categories list '%s' already registered" % identifier)
        return

    menu_types = []
    for cat in cat_list:
        if SUBCATEGORY_SEPARATOR in cat.identifier:
            prefix = "NODE_MT_subcategory_"
        else:
            prefix = "NODE_MT_category_"

        menu_type = type(prefix + cat.identifier, (bpy.types.Menu,), {
            "bl_space_type": 'NODE_EDITOR',
            "bl_label": cat.name,
            "category": cat,
            "poll": cat.poll,
            "draw": draw_node_item,
        })
        category_leaf = cat.identifier.replace(settings.ID_TREE_CATEGORY_TEMPLATE.format(""), "")
        if category_leaf in BUILD_CATEGORIES:
            old_draw_fn = menu_type.draw

            def draw(self, context):
                sub_category_names = {leaf.identifier for leaf in BUILD_CATEGORIES[self.bl_idname.split("_")[-1]]}
                layout = self.layout
                for name in sub_category_names:
                    layout.menu("NODE_MT_subcategory_{}".format(name), icon=CATEGORY_CONFIG_MAP[name.replace(settings.ID_TREE_CATEGORY_TEMPLATE.format(""), "")]["icon"])
                layout.separator()
                old_draw_fn(self, context)
                layout.separator()
                layout.label(text="Main category")
            menu_type.draw = draw
        menu_types.append(menu_type)

        bpy.utils.register_class(menu_type)

    # stores: (categories list, menu draw function, submenu types)
    _node_categories[identifier] = (cat_list, draw_add_menu, menu_types)


class AutoRegisterNodeCategories:
    _ocvl_auto_register = None
    register_mode = None
    node_classes_list = None
    node_categories_dict = None
    nodes_module_path = None

    def __init__(self, register_mode=True):
        self.register_mode = register_mode
        self._ocvl_auto_register = self._register_node if register_mode else self._unregister_node
        self.node_classes_list = []
        self.node_categories_dict = defaultdict(list)
        self.nodes_module_path = os.path.join(ocvl.__path__[0], settings.NAME_NODE_DIRECTORY)

        ocvl_path = ocvl.__path__[0]
        self.nodes_module_path = os.path.join(ocvl_path, settings.NAME_NODE_DIRECTORY)
        self.recursive_register(self.nodes_module_path, addon_module='ocvl')

        ocvl_pro_path = os.path.join(os.path.sep.join(ocvl_path.split(os.path.sep)[:-1]), settings.OCVL_PRO_DIR_NAME)
        if os.path.exists(ocvl_pro_path):
            self.nodes_module_path = os.path.join(ocvl_pro_path, settings.NAME_NODE_DIRECTORY)
            self.recursive_register(self.nodes_module_path, addon_module='ocvl_pro')
        self.end_register()

    def _register_node(self, *args, **kwargs):
        return register_node(*args, **kwargs)

    def _unregister_node(self, *args, **kwargs):
        return unregister_node(*args, **kwargs)

    def process_module(self, file_name, node_file_path, node_classes_list, _ocvl_auto_register, dir_category=False, addon_module="ocvl"):
        deep_import_path = ".".join(node_file_path.replace(self.nodes_module_path, "").split(os.sep)[1:-1])
        spec = util.spec_from_file_location("{}.{}.{}.{}".format(addon_module, settings.NAME_NODE_DIRECTORY, deep_import_path, file_name), node_file_path)
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if file_name.startswith(SUBCATEGORY_SEPARATOR) or file_name.startswith("abc"):
            return

        for obj_name in dir(mod):
            if is_node_class_name(obj_name):
                node_class = getattr(mod, obj_name)
                if dir_category:
                    node_class.n_category = deep_import_path
                    node_class.n_category = deep_import_path.replace(".", SUBCATEGORY_SEPARATOR)
                    exec("import {}.nodes.{}".format(addon_module, deep_import_path))
                    category_module_path = "{}.{}.{}".format(addon_module, settings.NAME_NODE_DIRECTORY, deep_import_path)
                    icon = eval("getattr({}, 'icon', 'NONE')".format(category_module_path))
                    name = eval("getattr({}, 'name', '{}')".format(category_module_path, node_class.n_category))
                    description = eval("getattr({}, 'description', '{}')".format(category_module_path, node_class.n_category))
                    CATEGORY_CONFIG_MAP[node_class.n_category] = {"icon": icon, "name": name, "description": description}

                if node_class.n_category:
                    node_classes_list.append(node_class)
                    _ocvl_auto_register(node_class)

    def recursive_register(self, module_path, addon_module='ocvl'):
        for file_name in os.listdir(module_path):
            if file_name in settings.BLACK_LIST_REGISTER_NODE_CATEGORY:
                continue

            node_file_path = node_file_path_in = os.path.join(module_path, file_name)
            if os.path.isfile(node_file_path):
                self.process_module(file_name, node_file_path, self.node_classes_list, self._ocvl_auto_register)
            elif os.path.isdir(node_file_path):
                for file_name_in in os.listdir(node_file_path_in):
                    if not file_name_in.startswith(SUBCATEGORY_SEPARATOR):
                        node_file_path_in = os.path.join(node_file_path, file_name_in)
                        if os.path.isfile(node_file_path_in):
                            self.process_module(file_name_in, node_file_path_in, self.node_classes_list, self._ocvl_auto_register, dir_category=True, addon_module=addon_module)
                self.recursive_register(node_file_path, addon_module=addon_module)

    def condition_registration_node(self, node_class):
        if node_class.n_development_status:
            if node_class.n_development_status == "BETA":
                return is_second_extension_path()
        else:
            return True
        return False

    def end_register(self):
        for node_class in self.node_classes_list:
            if self.condition_registration_node(node_class):
                node_class.n_category = node_class.n_category.replace(".", SUBCATEGORY_SEPARATOR)
                self.node_categories_dict[node_class.n_category].append(NodeItem(node_class.__name__, node_class.__name__[4:-4]))

        for category_name in self.node_categories_dict.keys():
            category_name = category_name.replace(".", SUBCATEGORY_SEPARATOR)
            if category_name == "uncategorized":
                continue

            node_category = OCVLNodeCategory(
                identifier=settings.ID_TREE_CATEGORY_TEMPLATE.format(category_name),
                name=CATEGORY_CONFIG_MAP[category_name]["name"],
                description=CATEGORY_CONFIG_MAP[category_name]["description"],
                items=self.node_categories_dict[category_name],
            )
            node_category.icon = CATEGORY_CONFIG_MAP[category_name]["icon"]
            if SUBCATEGORY_SEPARATOR in category_name:
                node_category.identifier = node_category.identifier.replace(".", SUBCATEGORY_SEPARATOR)
                BUILD_CATEGORIES["{}".format(category_name.split(SUBCATEGORY_SEPARATOR)[0])].append(node_category)
            else:
                BUILD_CATEGORIES[settings.OCVL_NODE_CATEGORIES].append(node_category)
        if self.register_mode:
            for key, value in BUILD_CATEGORIES.items():
                try:
                    register_node_categories(key, value)
                except KeyError as e:
                    logger.info("{} already registered.".format(settings.OCVL_NODE_CATEGORIES))
        else:
            unregister_node_categories(settings.OCVL_NODE_CATEGORIES)


def register():
    AutoRegisterNodeCategories(register_mode=True)


def unregister():
    AutoRegisterNodeCategories(register_mode=False)
