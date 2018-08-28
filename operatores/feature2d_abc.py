import bpy
from bpy.props import StringProperty

from ..globals import FEATURE2D_INSTANCES_DICT
from ..utils import cv_register_class, cv_unregister_class


class InitFeature2DOperator(bpy.types.Operator):
    bl_idname = "node.init_feature_2d"
    bl_label = "Init Feature 2D"

    origin = StringProperty("")

    @staticmethod
    def get_init_kwargs(node):
        kwargs_init = {}
        for key in dir(node):
            val = getattr(node, key)
            if key.endswith("_init") and isinstance(val, (int, float, str)):
                kwargs_init[key.replace("_init", "")] = val
        return kwargs_init

    @staticmethod
    def update_feature_instance_dict(node, node_tree, node_name):
        kwargs_init = InitFeature2DOperator.get_init_kwargs(node)
        instance = node._init_method(**kwargs_init)
        node.loc_class_repr = str(instance)
        FEATURE2D_INSTANCES_DICT["{}.{}".format(node_tree, node_name)] = instance

    def execute(self, context):
        node_tree, node_name, *props_name = self.origin.split('|><|')
        node = bpy.data.node_groups[node_tree].nodes[node_name]
        self.update_feature_instance_dict(node, node_tree, node_name)
        return {'FINISHED'}


def register():
    cv_register_class(InitFeature2DOperator)


def unregister():
    cv_unregister_class(InitFeature2DOperator)
