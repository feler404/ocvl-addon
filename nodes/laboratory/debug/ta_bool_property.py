import uuid

import bpy
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLBoolPropNode(OCVLNodeBase):

    n_doc = "Property debug."

    bool_0_PIXEL:      bpy.props.BoolProperty(default=True, subtype="PIXEL")
    bool_0_UNSIGNED:   bpy.props.BoolProperty(default=True, subtype="UNSIGNED")
    bool_0_PERCENTAGE: bpy.props.BoolProperty(default=True, subtype="PERCENTAGE")
    bool_0_FACTOR:     bpy.props.BoolProperty(default=True, subtype="FACTOR")
    bool_0_ANGLE:      bpy.props.BoolProperty(default=True, subtype="ANGLE")
    bool_0_TIME:       bpy.props.BoolProperty(default=True, subtype="TIME")
    bool_0_DISTANCE:   bpy.props.BoolProperty(default=True, subtype="DISTANCE")
    bool_0_NONE:       bpy.props.BoolProperty(default=True, subtype="NONE")

    bool_0_HIDDEN:           bpy.props.BoolProperty(default=True, subtype="NONE", options={"HIDDEN"})
    bool_0_SKIP_SAVE:        bpy.props.BoolProperty(default=True, subtype="NONE", options={"SKIP_SAVE"})
    bool_0_ANIMATABLE:       bpy.props.BoolProperty(default=True, subtype="NONE", options={"ANIMATABLE"})
    bool_0_LIBRARY_EDITABLE: bpy.props.BoolProperty(default=True, subtype="NONE", options={"LIBRARY_EDITABLE"})
    bool_0_PROPORTIONAL:     bpy.props.BoolProperty(default=True, subtype="NONE", options={"PROPORTIONAL"})
    bool_0_TEXTEDIT_UPDATE:  bpy.props.BoolProperty(default=True, subtype="NONE", options={"TEXTEDIT_UPDATE"})

    def init(self, context):
        self.width = 200
        self.inputs.new('OCVLObjectSocket', "bool_0_PIXEL").prop_name =      'bool_0_PIXEL'
        self.inputs.new('OCVLObjectSocket', "bool_0_UNSIGNED").prop_name =   'bool_0_UNSIGNED'
        self.inputs.new('OCVLObjectSocket', "bool_0_PERCENTAGE").prop_name = 'bool_0_PERCENTAGE'
        self.inputs.new('OCVLObjectSocket', "bool_0_FACTOR").prop_name =     'bool_0_FACTOR'
        self.inputs.new('OCVLObjectSocket', "bool_0_ANGLE").prop_name =      'bool_0_ANGLE'
        self.inputs.new('OCVLObjectSocket', "bool_0_TIME").prop_name =       'bool_0_TIME'
        self.inputs.new('OCVLObjectSocket', "bool_0_DISTANCE").prop_name =   'bool_0_DISTANCE'
        self.inputs.new('OCVLObjectSocket', "bool_0_NONE").prop_name =       'bool_0_NONE'

        self.inputs.new('OCVLObjectSocket', "bool_0_HIDDEN").prop_name =          'bool_0_HIDDEN'
        self.inputs.new('OCVLObjectSocket', "bool_0_SKIP_SAVE").prop_name =       'bool_0_SKIP_SAVE'
        self.inputs.new('OCVLObjectSocket', "bool_0_ANIMATABLE").prop_name =      'bool_0_ANIMATABLE'
        self.inputs.new('OCVLObjectSocket', "bool_0_LIBRARY_EDITABLE").prop_name ='bool_0_LIBRARY_EDITABLE'
        self.inputs.new('OCVLObjectSocket', "bool_0_PROPORTIONAL").prop_name =    'bool_0_PROPORTIONAL'
        self.inputs.new('OCVLObjectSocket', "bool_0_TEXTEDIT_UPDATE").prop_name = 'bool_0_TEXTEDIT_UPDATE'

    def wrapped_process(self):
        pass
