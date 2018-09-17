import uuid

import cv2
import numpy as np
from bpy.props import EnumProperty, StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode
from ...auth import ocvl_auth


class OCVLCustomInputNode(OCVLNode):
    ''' Input from custom input Python code.

    '''
    bl_icon = 'TEXT'




if ocvl_auth.ocvl_pro_version_auth:
    from ...extend.laboratory.ta_custom_input import OCVLCustomInputNode


def register():
    cv_register_class(OCVLCustomInputNode)


def unregister():
    cv_unregister_class(OCVLCustomInputNode)
