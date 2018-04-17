from ...utils import cv_register_class, cv_unregister_class
from ...extend.labolatory.cv_bitwise import OCVLBitwiseNode


def register():
    cv_register_class(OCVLBitwiseNode)


def unregister():
    cv_unregister_class(OCVLBitwiseNode)
