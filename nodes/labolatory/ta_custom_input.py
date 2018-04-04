from ...extend.labolatory.ta_custom_input import OCVLCustomInputNode
from ...extend.utils import cv_register_class, cv_unregister_class


def register():
    cv_register_class(OCVLCustomInputNode)


def unregister():
    cv_unregister_class(OCVLCustomInputNode)
