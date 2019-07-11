import uuid

import bpy
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLIntPropNode(OCVLNodeBase):

    n_doc = "Property debug."

    int_0_PIXEL:      bpy.props.IntProperty(default=100, min=-100, max=255, subtype="PIXEL")
    int_0_UNSIGNED:   bpy.props.IntProperty(default=100, min=-100, max=255, subtype="UNSIGNED")
    int_0_PERCENTAGE: bpy.props.IntProperty(default=100, min=-100, max=255, subtype="PERCENTAGE")
    int_0_FACTOR:     bpy.props.IntProperty(default=100, min=-100, max=255, subtype="FACTOR")
    int_0_ANGLE:      bpy.props.IntProperty(default=100, min=-100, max=255, subtype="ANGLE")
    int_0_TIME:       bpy.props.IntProperty(default=100, min=-100, max=255, subtype="TIME")
    int_0_DISTANCE:   bpy.props.IntProperty(default=100, min=-100, max=255, subtype="DISTANCE")
    int_0_NONE:       bpy.props.IntProperty(default=100, min=-100, max=255, subtype="NONE")

    def init(self, context):
        self.width = 200
        self.inputs.new('StringsSocket', "int_0_PIXEL").prop_name = 'int_0_PIXEL'
        self.inputs.new('StringsSocket', "int_0_UNSIGNED").prop_name = 'int_0_UNSIGNED'
        self.inputs.new('StringsSocket', "int_0_PERCENTAGE").prop_name = 'int_0_PERCENTAGE'
        self.inputs.new('StringsSocket', "int_0_FACTOR").prop_name = 'int_0_FACTOR'
        self.inputs.new('StringsSocket', "int_0_ANGLE").prop_name = 'int_0_ANGLE'
        self.inputs.new('StringsSocket', "int_0_TIME").prop_name = 'int_0_TIME'
        self.inputs.new('StringsSocket', "int_0_DISTANCE").prop_name = 'int_0_DISTANCE'
        self.inputs.new('StringsSocket', "int_0_NONE").prop_name = 'int_0_NONE'

    def wrapped_process(self):
        pass
