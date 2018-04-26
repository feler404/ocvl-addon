from ...utils import cv_register_class, cv_unregister_class
from ...auth import ocvl_auth

if ocvl_auth.ocvl_ext:
    from ...extend.laboratory.ta_custom_input import OCVLCustomInputNode

    def register():
        cv_register_class(OCVLCustomInputNode)


    def unregister():
        cv_unregister_class(OCVLCustomInputNode)
