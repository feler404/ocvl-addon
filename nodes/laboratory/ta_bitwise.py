from ...utils import cv_register_class, cv_unregister_class, OCVL_EXT

if OCVL_EXT:
    from ...extend.laboratory.ta_bitwise import OCVLBitwiseNode


    def register():
        cv_register_class(OCVLBitwiseNode)


    def unregister():
        cv_unregister_class(OCVLBitwiseNode)
