import bpy
from bpy.props import IntProperty
from ocvl.core.node_base import OCVLNode


class OCVLNode1(OCVLNode):
    bl_idname = "OCVLNode1"
    bl_label = "OCVLNode1"
    bl_icon = "COLOR"

    myStringProperty = bpy.props.StringProperty(subtype='FILE_PATH', default="//")

    # Custom enum property to select from a predefined list
    my_items = [
        ("DOWN", "Down", "Where your feet are"),
        ("UP", "Up", "Where your head should be"),
        ("LEFT", "Left", "Not right"),
        ("RIGHT", "Right", "Not left")
    ]
    myEnumProperty = bpy.props.EnumProperty(name="Direction", description="Just an example",
                                            items=my_items, default='UP')
    # my_input_value = bpy.props.FloatProperty(name="Size", default_value=5.0, subtype="Factor")

    surface = bpy.props.StringProperty(default="")


    def init(self, context):
        self.inputs.new('OCVLUUIDSocket', "Surface")#.prop_name = "surface"
        # self.inputs.new("NodeSocketFloat", "My Input").value_property = "my_input_value"
        # my_input.value_property = "my_input_value"

    def update(self):
        pass


class OCVLNode2(OCVLNode):
    bl_idname = "OCVLNode2"
    bl_label = "OCVLNode2"
    bl_icon = "COLOR"


    surface = bpy.props.StringProperty(default="asdfasdfa")


    def init(self, context):
        self.outputs.new('OCVLUUIDSocket', "Surface")

    def update(self):
        pass
