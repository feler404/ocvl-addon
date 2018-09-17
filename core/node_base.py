import bpy


class OCVLNode(bpy.types.Node):
    """
    BaseClass concept
    https://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined
    """
    ocvl_auto_register = True
    ocvl_category = "uncategorized"

