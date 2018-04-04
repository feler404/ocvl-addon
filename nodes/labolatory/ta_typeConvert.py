from ...extend.labolatory.ta_typeConvert import OCVLTypeConvertNode
from ...extend.utils import cv_register_class, cv_unregister_class


def register():
    cv_register_class(OCVLTypeConvertNode)


def unregister():
    cv_unregister_class(OCVLTypeConvertNode)
