import bpy

from ...extend.labolatory.ta_image_sample import OCVLImageImporterOpMK2, OCVLTakeImageFromCamera, OCVLImageSampleNode
from ...extend.utils import cv_register_class, cv_unregister_class


def register():
    cv_register_class(OCVLImageImporterOpMK2)
    cv_register_class(OCVLTakeImageFromCamera)
    cv_register_class(OCVLImageSampleNode)


def unregister():
    cv_unregister_class(OCVLImageSampleNode)
    cv_unregister_class(OCVLTakeImageFromCamera)
    cv_unregister_class(OCVLImageImporterOpMK2)

