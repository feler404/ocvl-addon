import bpy
from ocvl.core.constants import OCVL_NODE_TREE_TYPE
from ocvl.core.register_utils import ocvl_register, ocvl_unregister


class OCVLNodeTree(bpy.types.NodeTree):
    """
    Node tree consisting of linked nodes used for shading, textures and compositing.
    """

    bl_idname = OCVL_NODE_TREE_TYPE
    bl_label = "OCVL Group Tree type"
    bl_icon = "COLOR"


def register():
    ocvl_register(OCVLNodeTree)
    from ocvl.core.node_categories import register as node_categories_register
    node_categories_register()


def unregister():
    ocvl_unregister(OCVLNodeTree)
    from ocvl.core.node_categories import unregister as node_categories_unregister
    node_categories_unregister()
