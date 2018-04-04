import bpy

from ...extend.labolatory.ta_debug_node import OCVLTestNode, OCVLMsgPopUpOpenCVInfoInEditor, OCVLMsgPopUpOpenCVInfo
from ...extend.utils import cv_register_class, cv_unregister_class


def register():
    bpy.utils.register_class(OCVLMsgPopUpOpenCVInfo)
    bpy.utils.register_class(OCVLMsgPopUpOpenCVInfoInEditor)
    cv_register_class(OCVLTestNode)


def unregister():
    cv_unregister_class(OCVLTestNode)
    bpy.utils.unregister_class(OCVLMsgPopUpOpenCVInfoInEditor)
    bpy.utils.unregister_class(OCVLMsgPopUpOpenCVInfo)
