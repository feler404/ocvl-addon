import uuid

import bpy

from ocvl.core.globals import FEATURE2D_INSTANCES_DICT
from ocvl.operatores.abc import OCVL_OT_InitFeature2DOperator
from ocvl.core.node_base import update_node


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


class OCVLFeature2DMixIn:

    n_doc = ""
    n_requirements = {"__and__": ["image_in"]}
    _feature_class_type = 2  # 0 - for detect class, 1 - for compute class, 2 - for detect and compute class
    ABC_GLOBAL_INSTANCE_DICT_NAME = FEATURE2D_INSTANCES_DICT

    def update_layout(self, context):
        self.update_sockets(context)
        update_node(self, context)

    def update_and_init(self, context):
        OCVL_OT_InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_sockets(context)
        update_node(self, context)

    image_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="Input 8-bit or floating-point 32-bit, single-channel image.")
    mask_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="Optional region of interest.")
    keypoints_in: bpy.props.StringProperty(default=str(uuid.uuid4()), description="")

    keypoints_out: bpy.props.StringProperty(default=str(uuid.uuid4()), description="")
    descriptors_out: bpy.props.StringProperty(default=str(uuid.uuid4()), description="")

    loc_file_load: bpy.props.StringProperty(default="/", description="")
    loc_file_save: bpy.props.StringProperty(default="/", description="")
    loc_work_mode: bpy.props.EnumProperty(items=WORK_MODE_ITEMS, default="DETECT-COMPUTE", update=update_layout, description="")
    loc_state_mode: bpy.props.EnumProperty(items=STATE_MODE_ITEMS, default="INIT", update=update_layout, description="")
    loc_descriptor_size: bpy.props.IntProperty(default=0, description="")
    loc_descriptor_type: bpy.props.IntProperty(default=0, description="")
    loc_default_norm: bpy.props.IntProperty(default=0, description="")
    loc_class_repr: bpy.props.StringProperty(default="", description="")

    def init(self, context):
        self.width = 250
        self.inputs.new("OCVLImageSocket", "image_in")
        self.inputs.new("OCVLMaskSocket", "mask_in")
        self.inputs.new("OCVLObjectSocket", "keypoints_in")

        self.outputs.new("OCVLObjectSocket", "keypoints_out")
        self.outputs.new("OCVLObjectSocket", "descriptors_out")
        self.update_layout(context)
        OCVL_OT_InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name))

    def update_sockets(self, context):
        self.update_sockets_for_node_mode(WORK_MODE_PROPS_MAPS, self.loc_work_mode)

    def draw_buttons(self, context, layout):
        origin = self.get_node_origin()
        self.add_button(layout=layout, prop_name='loc_work_mode', expand=True, enabled=self._feature_class_type == 2)
        self.add_button(layout=layout, prop_name='loc_state_mode', expand=True, enabled=False)
        if self.loc_state_mode == "INIT":
            layout.operator("ocvl.init_feature_2d", icon='MENU_PANEL').origin = origin
            layout.label(text="Instance: {}".format(self.loc_class_repr))
            for key in OCVL_OT_InitFeature2DOperator.get_init_kwargs(self):
                arg_name = key
                if arg_name.startswith("_"):
                    arg_name = "T1" + arg_name
                layout.row().prop(self, "{}_init".format(arg_name))
        elif self.loc_state_mode == "LOAD":
            layout.row().prop(self, "loc_file_load")
        elif self.loc_state_mode == "SAVE":
            layout.row().prop(self, "loc_file_save")

    def free(self):
        FEATURE2D_INSTANCES_DICT.pop("{}.{}".format(self.id_data.name, self.name))
        super().free()

    def _detect(self, instance):
        self.check_input_requirements(["image_in"])
        kwargs = {
            'image': self.get_from_props("image_in"),
            'mask': None,
        }
        keypoints_out = self.process_cv(fn=instance.detect, kwargs=kwargs)
        self.refresh_output_socket("keypoints_out", keypoints_out, is_uuid_type=True)

    def _compute(self, instance):
        self.check_input_requirements(["image_in", "keypoints_in"])
        kwargs = {
            'image': self.get_from_props("image_in"),
            'keypoints': self.get_from_props("keypoints_in"),
        }

        keypoints_out, descriptors_out = self.process_cv(fn=instance.compute, kwargs=kwargs)
        self.refresh_output_socket("keypoints_out", keypoints_out, is_uuid_type=True)
        self.refresh_output_socket("descriptors_out", descriptors_out, is_uuid_type=True)

    def _detect_and_compute(self, instance):
        self.check_input_requirements(["image_in"])
        kwargs = {
            'image': self.get_from_props("image_in"),
            'mask': None,
        }
        keypoints_out, descriptors_out = self.process_cv(fn=instance.detectAndCompute, kwargs=kwargs)
        self.refresh_output_socket("keypoints_out", keypoints_out, is_uuid_type=True)
        self.refresh_output_socket("descriptors_out", descriptors_out, is_uuid_type=True)


class OCVLFeature2DDetectorMixIn(OCVLFeature2DMixIn):
    n_requirements = {"__and__": ["image_in"]}
    _feature_class_type = 0

    def update_layout(self, context):
        self.update_sockets(context)
        if FEATURE2D_INSTANCES_DICT.get("{}.{}".format(self.id_data.name, self.name)):
            update_node(self, context)

    def update_and_init(self, context):
        OCVL_OT_InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_sockets(context)
        update_node(self, context)

    loc_work_mode: bpy.props.EnumProperty(items=WORK_MODE_ITEMS, default="DETECT", update=update_layout, description="")


class OCVLFeature2CalculatorDMixIn(OCVLFeature2DMixIn):
    n_requirements = {"__and__": ["image_in", "keypoints_in"]}
    _feature_class_type = 1

    def update_layout(self, context):
        self.update_sockets(context)
        update_node(self, context)

    def update_and_init(self, context):
        OCVL_OT_InitFeature2DOperator.update_class_instance_dict(self, self.id_data.name, self.name)
        self.update_sockets(context)
        update_node(self, context)

    loc_work_mode: bpy.props.EnumProperty(items=WORK_MODE_ITEMS, default="COMPUTE", update=update_layout, description="")
