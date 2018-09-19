import uuid

import cv2
import numpy as np
import bpy

from ocvl.core.node_base import OCVLNodeBase, update_node
from ...auth import ocvl_auth


class OCVLCustomInputNode(OCVLNodeBase):
    ''' Input from custom input Python code.

    '''
    bl_icon = 'TEXT'




if ocvl_auth.ocvl_pro_version_auth:
    from ...extend.laboratory.ta_custom_input import OCVLCustomInputNode



