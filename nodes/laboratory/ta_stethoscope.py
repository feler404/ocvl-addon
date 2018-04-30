from ...utils import cv_register_class, cv_unregister_class
from ...auth import ocvl_auth

if ocvl_auth.ocvl_ext:
    from ...extend.laboratory.ta_stethoscope import OCVLStethoscopeNode

    def register():
        cv_register_class(OCVLStethoscopeNode)


    def unregister():
        cv_unregister_class(OCVLStethoscopeNode)
