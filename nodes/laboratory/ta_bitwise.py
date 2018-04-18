from ...utils import cv_register_class, cv_unregister_class
from ...auth import ocvl_auth

if ocvl_auth.ocvl_ext:
    from ...extend.laboratory.ta_bitwise import OCVLBitwiseNode


    def register():
        cv_register_class(OCVLBitwiseNode)


    def unregister():
        cv_unregister_class(OCVLBitwiseNode)
