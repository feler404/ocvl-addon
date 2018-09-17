import cv2
import uuid
import numpy as np
from gettext import gettext as _
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty

from ...globals import DESCRIPTORMATCHER_INSTANCES_DICT
from ...operatores.abc import InitDescriptorMatcherOperator
from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


WORK_MODE_ITEMS = (
    ("ADD", "ADD", "ADD", "", 0),
    ("CLEAR", "CLEAR", "CLEAR", "", 1),
    ("KNNMATCH", "KNNMATCH", "KNNMATCH", "", 2),
    ("MATCH", "MATCH", "MATCH", "", 3),
    # ("RADIUSMATCH", "RADIUSMATCH", "RADIUSMATCH", "", 4),
)

STATE_MODE_ITEMS = (
    ("INIT", "INIT", "INIT", "", 0),
    ("LOAD", "LOAD", "LOAD", "", 1),
    ("SAVE", "SAVE", "SAVE", "", 2),
)


STATE_MODE_PROPS_MAPS = {
    STATE_MODE_ITEMS[0][0]: tuple(),
    STATE_MODE_ITEMS[1][0]: ("loc_file_load",),
    STATE_MODE_ITEMS[2][0]: ("loc_file_save",),
}


WORK_MODE_PROPS_MAPS = {
    WORK_MODE_ITEMS[0][0]: ("descriptors_in",),
    WORK_MODE_ITEMS[1][0]: (),
    WORK_MODE_ITEMS[2][0]: ("queryDescriptors_in", "trainDescriptors_in", "k_in", "mask_in", "compactResult_in", "matches_out"),
    WORK_MODE_ITEMS[3][0]: ("queryDescriptors_in", "trainDescriptors_in", "mask_in", "matches_out"),
}


NORM_TYPE_ITEMS = (
    ("NORM_L1", "NORM_L1", "NORM_L1", "", 0),
    ("NORM_L2", "NORM_L2", "NORM_L2", "", 1),
    ("NORM_HAMMING", "NORM_HAMMING", "NORM_HAMMING", "", 2),
    ("NORM_HAMMING2", "NORM_HAMMING2", "NORM_HAMMING2", "", 3),
)


class OCVLFlannBasedMatcherNode(OCVLNode):

    _doc = _("Flann-based descriptor matcher.")
    _url = "https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html#matcher"
    _init_method = cv2.FlannBasedMatcher_create
    ABC_GLOBAL_INSTANCE_DICT_NAME = DESCRIPTORMATCHER_INSTANCES_DICT

    def update_layout(self, context):
        self.update_sockets(context)
        updateNode(self, context)

    queryDescriptors_in = StringProperty(default=str(uuid.uuid4()), description=_(""))
    trainDescriptors_in = StringProperty(default=str(uuid.uuid4()), update=updateNode, description=_(""))
    descriptors_in = StringProperty(default=str(uuid.uuid4()), update=updateNode, description=_(""))
    k_in = IntProperty(default=2, min=1, max=10)
    mask_in = StringProperty(default=str(uuid.uuid4()), description=_(""))
    compactResult_in = BoolProperty(default=False)

    loc_file_save = StringProperty(default="/", description=_(""))
    loc_file_load = StringProperty(default="/", description=_(""))
    loc_work_mode = EnumProperty(items=WORK_MODE_ITEMS, default="MATCH", update=update_layout, description=_(""))
    loc_state_mode = EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description=_(""))
    loc_default_norm = IntProperty(default=0, description=_(""))
    loc_class_repr = StringProperty(default="", description=_(""))

    # trees_init = IntProperty(default=4, min=1, max=20, update=updateNode, description=_(""))
    # checks_init = IntProperty(default=32, min=2, max=128, update=updateNode, description=_(""))
    # eps_init = FloatProperty(default=0., min=0., max=1., update=updateNode, description=_(""))
    # sorted_init = BoolProperty(default=True, update=updateNode, description=_(""))

    matches_out = StringProperty(default=str(uuid.uuid4()), description=_(""))

    def sv_init(self, context):
        self.width = 250
        self.inputs.new("StringsSocket", "queryDescriptors_in")
        self.inputs.new("StringsSocket", "trainDescriptors_in")
        self.inputs.new("StringsSocket", "mask_in")

        self.outputs.new("StringsSocket", "matches_out")
        InitDescriptorMatcherOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_layout(context)

    def update_sockets(self, context):
        self.update_sockets_for_node_mode(WORK_MODE_PROPS_MAPS, self.loc_work_mode)
        self.process()

    def wrapped_process(self):
        self.check_input_requirements(["queryDescriptors_in", "trainDescriptors_in"])

        kwargs_detect = self.clean_kwargs({
            "queryDescriptors_in": self.get_from_props("queryDescriptors_in"),
            "trainDescriptors_in": self.get_from_props("trainDescriptors_in"),
        })

        fbm = DESCRIPTORMATCHER_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))
        matches_out = self.process_cv(fn=fbm.match, kwargs=kwargs_detect)
        self.refresh_output_socket("matches_out", matches_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        origin = self.get_node_origin()
        self.add_button(layout=layout, prop_name='loc_work_mode', expand=True)
        self.add_button(layout=layout, prop_name='loc_state_mode', expand=True)
        if self.loc_state_mode == "INIT":
            layout.operator("node.init_feature_2d", icon='MENU_PANEL').origin = origin
            layout.label("Instance: {}".format(self.loc_class_repr))
            for key in InitDescriptorMatcherOperator.get_init_kwargs(self):
                layout.row().prop(self, "{}_init".format(key))
        elif self.loc_state_mode == "LOAD":
            layout.row().prop(self, "loc_file_load")
        elif self.loc_state_mode == "SAVE":
            layout.row().prop(self, "loc_file_save")


def register():
    cv_register_class(OCVLFlannBasedMatcherNode)


def unregister():
    cv_unregister_class(OCVLFlannBasedMatcherNode)
