import uuid

import bpy
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLFloatPropNode(OCVLNodeBase):

    n_doc = "Property debug."

    float_0_PIXEL:      bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="PIXEL")
    float_0_UNSIGNED:   bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="UNSIGNED")
    float_0_PERCENTAGE: bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="PERCENTAGE")
    float_0_FACTOR:     bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="FACTOR")
    float_0_ANGLE:      bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="ANGLE")
    float_0_TIME:       bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="TIME")
    float_0_DISTANCE:   bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="DISTANCE")
    float_0_NONE:       bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="NONE")

    float_0_DISTANCE_NONE:         bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="DISTANCE", unit="NONE")
    float_0_DISTANCE_LENGTH:       bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="DISTANCE", unit="LENGTH")
    float_0_DISTANCE_AREA:         bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="DISTANCE", unit="AREA")
    float_0_DISTANCE_VOLUME:       bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="DISTANCE", unit="VOLUME")
    float_0_DISTANCE_ROTATION:     bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="DISTANCE", unit="ROTATION")
    float_0_DISTANCE_TIME:         bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="DISTANCE", unit="TIME")
    float_0_DISTANCE_VELOCITY:     bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="DISTANCE", unit="VELOCITY")
    float_0_DISTANCE_ACCELERATION: bpy.props.FloatProperty(default=100, min=-100, max=255, subtype="DISTANCE", unit="ACCELERATION")


    def init(self, context):
        self.width = 300
        self.inputs.new('OCVLMatrixSocket', "float_0_PIXEL").prop_name =      'float_0_PIXEL'
        self.inputs.new('OCVLMatrixSocket', "float_0_UNSIGNED").prop_name =   'float_0_UNSIGNED'
        self.inputs.new('OCVLMatrixSocket', "float_0_PERCENTAGE").prop_name = 'float_0_PERCENTAGE'
        self.inputs.new('OCVLMatrixSocket', "float_0_FACTOR").prop_name =     'float_0_FACTOR'
        self.inputs.new('OCVLMatrixSocket', "float_0_ANGLE").prop_name =      'float_0_ANGLE'
        self.inputs.new('OCVLMatrixSocket', "float_0_TIME").prop_name =       'float_0_TIME'
        self.inputs.new('OCVLMatrixSocket', "float_0_DISTANCE").prop_name =   'float_0_DISTANCE'
        self.inputs.new('OCVLMatrixSocket', "float_0_NONE").prop_name =       'float_0_NONE'

        self.inputs.new('OCVLMatrixSocket', "float_0_DISTANCE_NONE").prop_name =         'float_0_DISTANCE_NONE'
        self.inputs.new('OCVLMatrixSocket', "float_0_DISTANCE_LENGTH").prop_name =       'float_0_DISTANCE_LENGTH'
        self.inputs.new('OCVLMatrixSocket', "float_0_DISTANCE_AREA").prop_name =         'float_0_DISTANCE_AREA'
        self.inputs.new('OCVLMatrixSocket', "float_0_DISTANCE_VOLUME").prop_name =       'float_0_DISTANCE_VOLUME'
        self.inputs.new('OCVLMatrixSocket', "float_0_DISTANCE_ROTATION").prop_name =     'float_0_DISTANCE_ROTATION'
        self.inputs.new('OCVLMatrixSocket', "float_0_DISTANCE_TIME").prop_name =         'float_0_DISTANCE_TIME'
        self.inputs.new('OCVLMatrixSocket', "float_0_DISTANCE_VELOCITY").prop_name =     'float_0_DISTANCE_VELOCITY'
        self.inputs.new('OCVLMatrixSocket', "float_0_DISTANCE_ACCELERATION").prop_name = 'float_0_DISTANCE_ACCELERATION'

    def wrapped_process(self):
        pass
