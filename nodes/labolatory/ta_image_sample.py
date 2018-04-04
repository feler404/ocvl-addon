import bpy

from ...extend.labolatory.ta_image_sample import OCVLImageImporterOpMK2, OCVLTakeImageFromCamera, OCVLImageSampleNode
from ...extend.utils import cv_register_class, cv_unregister_class


def register():
    bpy.utils.register_class(OCVLImageImporterOpMK2)
    bpy.utils.register_class(OCVLTakeImageFromCamera)
    cv_register_class(OCVLImageSampleNode)


def unregister():
    bpy.utils.unregister_class(OCVLImageSampleNode)
    bpy.utils.register_class(OCVLTakeImageFromCamera)
    cv_unregister_class(OCVLImageImporterOpMK2)

