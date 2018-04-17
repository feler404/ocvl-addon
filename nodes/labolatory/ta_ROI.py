from ...extend.labolatory.ta_ROI import OCVLROINode
from ...utils import cv_register_class, cv_unregister_class


def register():
    cv_register_class(OCVLROINode)


def unregister():
    cv_unregister_class(OCVLROINode)
