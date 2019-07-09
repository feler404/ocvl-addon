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


class OCVLNodeCategory(NodeCategory):
    icon = "NONE"

    @classmethod
    def pull(cls, context):
        logger.info("Categories Node pull")
        return context.space_data.tree_type == constants.OCVL_NODE_TREE_TYPE


def is_node_class_name(class_name):
    return class_name.startswith(constants.PREFIX_NODE_CLASS) and \
           class_name.endswith(constants.SUFFIX_NODE_CLASS) and \
           class_name not in constants.BLACKLIST_FOR_REGISTER_NODE


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
                layout.menu("NODE_MT_category_%s" % cat.identifier, cat.icon)

    if identifier in _node_categories:
        raise KeyError("Node categories list '%s' already registered" % identifier)
        return

    menu_types = []
    for cat in cat_list:
        menu_type = type("NODE_MT_category_" + cat.identifier, (bpy.types.Menu,), {
            "bl_space_type": 'NODE_EDITOR',
            "bl_label": cat.name,
            "category": cat,
            "poll": cat.poll,
            "draw": draw_node_item,
        })

        menu_types.append(menu_type)

        bpy.utils.register_class(menu_type)

    # stores: (categories list, menu draw function, submenu types)
    _node_categories[identifier] = (cat_list, draw_add_menu, menu_types)


class AutoRegisterNodeCategories:
    _ocvl_auto_register = None
    register_mode = None
    node_classes_list = None
    node_categories_dict = None
    build_categories = None
    nodes_module_path = None

    def __init__(self, register_mode=True):
        self.register_mode = register_mode
        self._ocvl_auto_register = self._register_node if register_mode else self._unregister_node
        self.node_classes_list = []
        self.node_categories_dict = defaultdict(list)
        self.build_categories = []
        self.nodes_module_path = os.path.join(ocvl.__path__[0], constants.NAME_NODE_DIRECTORY)
        self.register()

    def _register_node(self, *args, **kwargs):
        return register_node(*args, **kwargs)

    def _unregister_node(self, *args, **kwargs):
        return unregister_node(*args, **kwargs)

    def process_module(self, file_name, node_file_path, node_classes_list, _ocvl_auto_register, dir_category=False):
        spec = util.spec_from_file_location("ocvl.{}.{}".format(constants.NAME_NODE_DIRECTORY, file_name), node_file_path)
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for obj_name in dir(mod):
            if is_node_class_name(obj_name):
                node_class = getattr(mod, obj_name)
                if dir_category:
                    node_class.n_category = node_file_path.split(os.sep)[-2]
                if node_class.n_category and node_class.n_auto_register:
                    node_classes_list.append(node_class)
                    _ocvl_auto_register(node_class)

    def register(self):
        for file_name in os.listdir(self.nodes_module_path):
            if file_name in BLACK_LIST_REGISTER_NODE_CATEGORY:
                continue

            if not file_name.startswith("__"):
                node_file_path = node_file_path_in = os.path.join(self.nodes_module_path, file_name)
                if os.path.isfile(node_file_path):
                    self.process_module(file_name, node_file_path, self.node_classes_list, self._ocvl_auto_register)
                elif os.path.isdir(node_file_path):
                    for file_name_in in os.listdir(node_file_path_in):
                        if not file_name_in.startswith("__"):
                            node_file_path_in = os.path.join(node_file_path, file_name_in)
                            if os.path.isfile(node_file_path_in):
                                self.process_module(file_name_in, node_file_path_in, self.node_classes_list, self._ocvl_auto_register, dir_category=True)

        for node_class in self.node_classes_list:
            self.node_categories_dict[node_class.n_category].append(NodeItem(node_class.__name__, node_class.__name__[4:-4]))

        for category_name in self.node_categories_dict.keys():
            node_category = OCVLNodeCategory(
                identifier=constants.ID_TREE_CATEGORY_TEMPLATE.format(category_name),
                name=category_name,
                description=category_name,
                items=self.node_categories_dict[category_name],
            )
            node_category.icon = "GHOST_DISABLED"
            self.build_categories.append(node_category)

        if self.register_mode:
            try:
                register_node_categories(constants.OCVL_NODE_CATEGORIES, self.build_categories)
            except KeyError as e:
                logger.info("{} already registered.".format(constants.OCVL_NODE_CATEGORIES))
        else:
            unregister_node_categories(constants.OCVL_NODE_CATEGORIES)


def register():
    AutoRegisterNodeCategories(register_mode=True)


def unregister():
    AutoRegisterNodeCategories(register_mode=False)
