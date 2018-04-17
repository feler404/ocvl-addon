from ...utils import cv_register_class, cv_unregister_class, OCVL_EXT

if OCVL_EXT:
    from ...extend.laboratory.ta_custom_input import OCVLCustomInputNode

    def register():
        cv_register_class(OCVLCustomInputNode)


    def unregister():
        cv_unregister_class(OCVLCustomInputNode)
