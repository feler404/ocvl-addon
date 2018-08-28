import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from ...globals import FEATURE2D_INSTANCES_DICT
from ...operatores.feature2d_abc import InitFeature2DOperator
from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


WORK_MODE_ITEMS = (
    ("DETECT", "DETECT", "DETECT", "", 0),
    ("COMPUTE", "COMPUTE", "COMPUTE", "", 1),
    ("DETECT-COMPUTE", "DETECT-COMPUTE", "DETECT-COMPUTE", "", 2),
)

STATE_MODE_ITEMS = (
    ("INIT", "INIT", "INIT", "", 0),
    ("LOAD", "LOAD", "LOAD", "", 1),
    ("SAVE", "SAVE", "SAVE", "", 2),
)

WORK_MODE_PROPS_MAPS = {
    WORK_MODE_ITEMS[0][0]: ("image_in", "mask_in", "keypoints_out"),
    WORK_MODE_ITEMS[1][0]: ("image_in", "keypoints_in", "keypoints_out", "descriptors_out"),
    WORK_MODE_ITEMS[2][0]: ("image_in", "mask_in", "keypoints_out", "descriptors_out"),
}

STATE_MODE_PROPS_MAPS = {
    STATE_MODE_ITEMS[0][0]: tuple(),
    STATE_MODE_ITEMS[1][0]: ("loc_file_load",),
    STATE_MODE_ITEMS[2][0]: ("loc_file_save",),
}


class OCVLFeature2DNode(OCVLNode):

    _doc = _("")

    def update_layout(self, context):
        self.update_sockets(context)
        updateNode(self, context)

    image_in = StringProperty(default=str(uuid.uuid4()), description=_("Input 8-bit or floating-point 32-bit, single-channel image."))
    mask_in = StringProperty(default=str(uuid.uuid4()), description=_("Optional region of interest."))
    keypoints_in = StringProperty(default=str(uuid.uuid4()), description=_(""))

    keypoints_out = StringProperty(default=str(uuid.uuid4()), description=_(""))
    descriptors_out = StringProperty(default=str(uuid.uuid4()), description=_(""))

    loc_file_load = StringProperty(default="/", description=_(""))
    loc_file_save = StringProperty(default="/", description=_(""))
    loc_work_mode = EnumProperty(items=WORK_MODE_ITEMS, default="DETECT-COMPUTE", update=update_layout, description=_(""))
    loc_state_mode = EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description=_(""))
    loc_descriptor_size = IntProperty(default=0, description=_(""))
    loc_descriptor_type = IntProperty(default=0, description=_(""))
    loc_default_norm = IntProperty(default=0, description=_(""))
    loc_class_repr = StringProperty(default="", description=_(""))

    def sv_init(self, context):
        self.width = 250
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "mask_in")
        self.inputs.new("StringsSocket", "keypoints_in")

        self.outputs.new("StringsSocket", "keypoints_out")
        self.outputs.new("StringsSocket", "descriptors_out")
        InitFeature2DOperator.update_feature_instance_dict(self, self.id_data.name, self.name)
        FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))
        self.update_layout(context)

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

    def update_sockets(self, context):
        self.update_sockets_for_node_mode(WORK_MODE_PROPS_MAPS, self.loc_work_mode)
        self.process()

    def draw_buttons(self, context, layout):
        origin = self.get_node_origin()
        self.add_button(layout=layout, prop_name='loc_work_mode', expand=True)
        self.add_button(layout=layout, prop_name='loc_state_mode', expand=True)
        if self.loc_state_mode == "INIT":
            layout.operator("node.init_feature_2d", icon='MENU_PANEL').origin = origin
            layout.label("Instance: {}".format(self.loc_class_repr))
            for key in InitFeature2DOperator.get_init_kwargs(self):
                layout.row().prop(self, "{}_init".format(key))
        elif self.loc_state_mode == "LOAD":
            layout.row().prop(self, "loc_file_load")
        elif self.loc_state_mode == "SAVE":
            layout.row().prop(self, "loc_file_save")

def register():
    cv_register_class(OCVLFeature2DNode)


def unregister():
    cv_unregister_class(OCVLFeature2DNode)
