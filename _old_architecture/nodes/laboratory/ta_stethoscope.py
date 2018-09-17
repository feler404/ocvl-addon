from ...utils import cv_register_class, cv_unregister_class, OCVLNode, DEVELOP_STATE_BETA
from ...auth import ocvl_auth


class OCVLStethoscopeNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA


if ocvl_auth.ocvl_pro_version_auth:
    from ...extend.laboratory.ta_stethoscope import OCVLStethoscopeNode


def register():
    cv_register_class(OCVLStethoscopeNode)


def unregister():
    cv_unregister_class(OCVLStethoscopeNode)
