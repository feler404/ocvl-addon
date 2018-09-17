import os
from collections import defaultdict
from importlib import util
import ocvl
from ocvl.core.constants import OCVL_NODE_CATEGORIES, OCVL_NODE_TREE_TYPE
from ocvl.core.register_utils import ocvl_register, ocvl_unregister
from nodeitems_utils import (
    NodeCategory, NodeItem, register_node_categories, unregister_node_categories,
)


class OCVLNodeCategory(NodeCategory):

    @classmethod
    def pull(cls, context):
        return context.space_data.tree_type == OCVL_NODE_TREE_TYPE


def autoregister_node_categories(register_mode=True):
    _ocvl_auto_register = ocvl_register if register_mode else ocvl_unregister
    _auto_register_node_categories = register_node_categories if register_mode else unregister_node_categories

    node_classes_list = []
    node_categories_dict = defaultdict(list)
    build_categories = []
    nodes_module_path = os.path.join(ocvl.__path__[0], "nodes")
    for file_name in os.listdir(nodes_module_path):
        if not file_name.startswith("__"):
            node_file_path = os.path.join(nodes_module_path, file_name)
            if os.path.isfile(node_file_path):
                spec = util.spec_from_file_location("ocvl.nodes.{}".format(file_name), node_file_path)
                mod = util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                for obj_name in dir(mod):
                    if obj_name.startswith("OCVLNode") and obj_name != "OCVLNode":
                        node_class = getattr(mod, obj_name)
                        node_classes_list.append(node_class)
                        _ocvl_auto_register(node_class)

    for node_class in node_classes_list:
        node_categories_dict[node_class.ocvl_category].append(NodeItem(node_class.__name__))

    for category_name in node_categories_dict.keys():
        build_categories.append(OCVLNodeCategory(
            identifier="OCVL_CATEGORY_{}".format(category_name),
            name=category_name,
            description=category_name,
            items=node_categories_dict[category_name]
        ))

    _auto_register_node_categories(OCVL_NODE_CATEGORIES, build_categories)


def register():
    ocvl_register(OCVLNodeCategory)
    autoregister_node_categories(register_mode=True)


def unregister():
    ocvl_unregister(OCVLNodeCategory)
    autoregister_node_categories(register_mode=False)
