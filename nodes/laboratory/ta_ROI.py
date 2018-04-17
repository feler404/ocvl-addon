from ...utils import cv_register_class, cv_unregister_class, OCVL_EXT

if OCVL_EXT:
    from ...extend.laboratory.ta_ROI import OCVLROINode

    def register():
        cv_register_class(OCVLROINode)


    def unregister():
        cv_unregister_class(OCVLROINode)
