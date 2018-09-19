from ocvl.core.node_base import OCVLNodeBase, update_node
from ...auth import ocvl_auth


class OCVLTypeConvertNode(OCVLNodeBase):
    bl_develop_state = DEVELOP_STATE_BETA
if ocvl_auth.ocvl_pro_version_auth:
    from ...extend.laboratory.ta_typeConvert import OCVLTypeConvertNode
