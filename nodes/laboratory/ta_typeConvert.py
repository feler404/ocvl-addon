from ...utils import cv_register_class, cv_unregister_class, OCVL_EXT

if OCVL_EXT:
    from ...extend.laboratory.ta_typeConvert import OCVLTypeConvertNode


    def register():
        cv_register_class(OCVLTypeConvertNode)


    def unregister():
        cv_unregister_class(OCVLTypeConvertNode)
