import bpy

from ...extend.labolatory.ta_debug_node import OCVLTestNode, OCVLMsgPopUpOpenCVInfoInEditor, OCVLMsgPopUpOpenCVInfo
from ...utils import cv_register_class, cv_unregister_class


def register():
    cv_register_class(OCVLMsgPopUpOpenCVInfo)
    cv_register_class(OCVLMsgPopUpOpenCVInfoInEditor)
    cv_register_class(OCVLTestNode)


def unregister():
    cv_unregister_class(OCVLTestNode)
    cv_unregister_class(OCVLMsgPopUpOpenCVInfoInEditor)
    cv_unregister_class(OCVLMsgPopUpOpenCVInfo)
