import logging
import os

import bpy
from collections import defaultdict
from importlib import util
from nodeitems_utils import NodeCategory, NodeItem, unregister_node_categories, _node_categories # register_node_categories

import ocvl
from ocvl.core import constants
from ocvl.core.register_utils import register_node, unregister_node
from ocvl.core.settings import BLACK_LIST_REGISTER_NODE_CATEGORY

logger = logging.getLogger(__name__)


CATEGORY_CONFIG_MAP = {}  # icon, name, description
BUILD_CATEGORIES = defaultdict(lambda: [])
SUBCATEGORY_SEPARATOR = "."


class OCVLNodeCategory(NodeCategory):
    icon = None
    name = None
    description = None

    @classmethod
    def pull(cls, context):
        logger.info("Categories Node pull")
        return context.space_data.tree_type == constants.OCVL_NODE_TREE_TYPE


def is_node_class_name(class_name):
    return class_name.startswith(constants.PREFIX_NODE_CLASS) and \
           class_name.endswith(constants.SUFFIX_NODE_CLASS) and \
           class_name not in constants.BLACK_LIST_FOR_REGISTER_NODE


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
        category_leaf = cat.identifier.replace(constants.ID_TREE_CATEGORY_TEMPLATE.format(""), "")
        if category_leaf in BUILD_CATEGORIES:
            old_draw_fn = menu_type.draw

            def draw(self, context):
                sub_category_names = {leaf.identifier for leaf in BUILD_CATEGORIES[self.bl_idname.split("_")[-1]]}
                layout = self.layout
                for name in sub_category_names:
                    layout.menu("NODE_MT_subcategory_{}".format(name), icon=CATEGORY_CONFIG_MAP[name.replace(constants.ID_TREE_CATEGORY_TEMPLATE.format(""), "")]["icon"])
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
        self.nodes_module_path = os.path.join(ocvl.__path__[0], constants.NAME_NODE_DIRECTORY)

        self.recursive_register(self.nodes_module_path)
        self.end_register()

    def _register_node(self, *args, **kwargs):
        return register_node(*args, **kwargs)

    def _unregister_node(self, *args, **kwargs):
        return unregister_node(*args, **kwargs)

    def process_module(self, file_name, node_file_path, node_classes_list, _ocvl_auto_register, dir_category=False):
        deep_import_path = ".".join(node_file_path.replace(self.nodes_module_path, "").split(os.sep)[1:-1])
        spec = util.spec_from_file_location("ocvl.{}.{}.{}".format(constants.NAME_NODE_DIRECTORY, deep_import_path, file_name), node_file_path)
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if file_name.startswith("__") or file_name.startswith("abc"):
            return

        for obj_name in dir(mod):
            if is_node_class_name(obj_name):
                node_class = getattr(mod, obj_name)
                if dir_category:
                    node_class.n_category = deep_import_path
                    exec("import ocvl.nodes.{}".format(node_class.n_category))
                    category_module_path = "ocvl.{}.{}".format(constants.NAME_NODE_DIRECTORY, node_class.n_category)
                    icon = eval("getattr({}, 'icon', 'NONE')".format(category_module_path))
                    name = eval("getattr({}, 'name', '{}')".format(category_module_path, node_class.n_category))
                    description = eval("getattr({}, 'description', '{}')".format(category_module_path, node_class.n_category))
                    CATEGORY_CONFIG_MAP[node_class.n_category] = {"icon": icon, "name": name, "description": description}

                if node_class.n_category and node_class.n_auto_register:
                    node_classes_list.append(node_class)
                    _ocvl_auto_register(node_class)

    def recursive_register(self, module_path):
        for file_name in os.listdir(module_path):
            if file_name in BLACK_LIST_REGISTER_NODE_CATEGORY:
                continue

            node_file_path = node_file_path_in = os.path.join(module_path, file_name)
            if os.path.isfile(node_file_path):
                self.process_module(file_name, node_file_path, self.node_classes_list, self._ocvl_auto_register)
            elif os.path.isdir(node_file_path):
                for file_name_in in os.listdir(node_file_path_in):
                    if not file_name_in.startswith("__"):
                        node_file_path_in = os.path.join(node_file_path, file_name_in)
                        if os.path.isfile(node_file_path_in):
                            self.process_module(file_name_in, node_file_path_in, self.node_classes_list, self._ocvl_auto_register, dir_category=True)
                self.recursive_register(node_file_path)

    def end_register(self):
        for node_class in self.node_classes_list:
            self.node_categories_dict[node_class.n_category].append(NodeItem(node_class.__name__, node_class.__name__[4:-4]))

        for category_name in self.node_categories_dict.keys():
            if category_name == "uncategorized":
                continue
            node_category = OCVLNodeCategory(
                identifier=constants.ID_TREE_CATEGORY_TEMPLATE.format(category_name),
                name=CATEGORY_CONFIG_MAP[category_name]["name"],
                description=CATEGORY_CONFIG_MAP[category_name]["description"],
                items=self.node_categories_dict[category_name],
            )
            node_category.icon = CATEGORY_CONFIG_MAP[category_name]["icon"]
            if SUBCATEGORY_SEPARATOR in category_name:
                BUILD_CATEGORIES["{}".format(category_name.split(SUBCATEGORY_SEPARATOR)[0])].append(node_category)
            else:
                BUILD_CATEGORIES[constants.OCVL_NODE_CATEGORIES].append(node_category)

        if self.register_mode:
            for key, value in BUILD_CATEGORIES.items():
                try:
                    register_node_categories(key, value)
                except KeyError as e:
                    logger.info("{} already registered.".format(constants.OCVL_NODE_CATEGORIES))
        else:
            unregister_node_categories(constants.OCVL_NODE_CATEGORIES)


def register():
    AutoRegisterNodeCategories(register_mode=True)


def unregister():
    AutoRegisterNodeCategories(register_mode=False)

