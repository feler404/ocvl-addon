from ...extend.labolatory.ta_ROI import OCVLROINode
from ...extend.utils import cv_register_class, cv_unregister_class


def register():
    cv_register_class(OCVLROINode)


def unregister():
    cv_unregister_class(OCVLROINode)
