from ...extend.labolatory.cv_stethoscope import OCVLStethoscopeNode
from ...utils import cv_register_class, cv_unregister_class


def register():
    cv_register_class(OCVLStethoscopeNode)


def unregister():
    cv_unregister_class(OCVLStethoscopeNode)
