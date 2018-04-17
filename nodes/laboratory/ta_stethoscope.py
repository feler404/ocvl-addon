from ...utils import cv_register_class, cv_unregister_class, OCVL_EXT

if OCVL_EXT:
    from ...extend.laboratory.ta_stethoscope import OCVLStethoscopeNode

    def register():
        cv_register_class(OCVLStethoscopeNode)


    def unregister():
        cv_unregister_class(OCVLStethoscopeNode)
