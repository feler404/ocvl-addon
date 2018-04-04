from ...extend.labolatory.ta_viewer_image import OCVLImageViewerNode
from ...extend.utils import cv_register_class, cv_unregister_class


def register():
    cv_register_class(OCVLImageViewerNode)


def unregister():
    cv_unregister_class(OCVLImageViewerNode)

