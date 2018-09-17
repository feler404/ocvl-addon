from ...utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA
from ...auth import ocvl_auth


class OCVLBitwiseNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA


if ocvl_auth.ocvl_pro_version_auth:
    from ...extend.laboratory.ta_bitwise import OCVLBitwiseNode


def register():
    cv_register_class(OCVLBitwiseNode)


def unregister():
    cv_unregister_class(OCVLBitwiseNode)
