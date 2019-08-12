import inspect
import sys
import uuid
import cv2
import bpy
import numpy as np


from ocvl.core.node_base import OCVLNodeBase
from ocvl.core.globals import SOCKET_DATA_CACHE


array_256_repr = """
import cv2
import numpy as np
var = np.array([ 
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170,  190,  210,  230,  250,
10,  30,  50,  70,  90,  110,  130,  150,  170
], np.uint8)
"""

array_zeros_100x100 = """
import cv2
import numpy as np
var = np.zeros((100,100,3), np.uint8)
"""

array_ones_100x100 = """
import cv2
import numpy as np
var = np.ones((100,100,4), np.uint8)
"""

INPUT_TEMPLATES_ITEMS = [
    ("None", "None", "None", "", 0),
    (array_256_repr, "array_256_repr", "array_256_repr", "", 1),
    (array_zeros_100x100, "array_zeros_100x100", "array_zeros_100x100", "", 2),
    (array_ones_100x100, "array_ones_100x100", "array_ones_100x100", "", 3),
]

INPUT_NAME_TEMPLATE = "val_in_{}"


class OCVLCustomInputNode(OCVLNodeBase):

    n_doc = "Custom Python code input."
    n_requirements = {}

    def update_layout(self, context):
        self.update_sockets(context)
        self.process()

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()))
    val_in: bpy.props.StringProperty(default=str(uuid.uuid4()), update=update_layout)
    loc_vars_code: bpy.props.StringProperty(update=update_layout)
    loc_template: bpy.props.EnumProperty(items=INPUT_TEMPLATES_ITEMS, default="None", update=update_layout, description="Template for custom input")

    def init(self, context):
        self.width = 200
        self.inputs.new("OCVLImageSocket", "image_in")
        self.inputs.new("OCVLMatrixSocket", INPUT_NAME_TEMPLATE.format(0))
        text = bpy.data.texts.get(self.name)
        if not text:
            bpy.data.texts.new(self.name)
            text = bpy.data.texts[self.name]
            text.write("\n")
            text.write("import cv2\n")
            text.write("import numpy as np\n")
            text.write("my_output=1\n")
        self.loc_vars_code = self.name

    def wrapped_process(self):
        # loc_template = self.get_from_props("loc_template")
        # if loc_template != "None":
        #     for template_item in INPUT_TEMPLATES_ITEMS:
        #         if template_item[1] == loc_template:
        #             self.loc_vars_code = INPUT_TEMPLATES_ITEMS[0]

        self._refresh_inputs()
        context = self._get_context()
        old_locals = set(context.keys())

        loc_vars_code = "\n".join([line.body for line in bpy.data.texts.get(self.name).lines])
        try:
            exec(loc_vars_code, {}, context)
            self.n_error = ""
        except Exception as e:

            self.n_error =  str(e)
            self.n_error_line = inspect.getinnerframes(sys.exc_info()[2])[-1].lineno
            raise
        new_vars = set(context.keys()) - old_locals

        for socket_name in self.outputs.keys():
            if socket_name in ["image_out", "points_out", 'loc_vars_code']:
                continue
            if socket_name not in new_vars:
                self.outputs.remove(self.outputs[socket_name])
        for var_name in new_vars:
            socket_name = var_name
            if socket_name not in self.outputs:
                self.outputs.new("OCVLMatrixSocket", socket_name)
            var_value = context[var_name]
            if self.is_uuid(var_value) and var_value in SOCKET_DATA_CACHE:
                var_value = SOCKET_DATA_CACHE[var_value]
            is_uuid_type = isinstance(var_value, np.ndarray)
            self.refresh_output_socket(socket_name, var_value, is_uuid_type=is_uuid_type)

    def draw_buttons(self, context, layout):
        # self.add_button(layout, prop_name="loc_template", icon="COPY_ID")
        row = layout.row(align=True)
        if self.text_block:
            layout.operator("an.select_area", text="Show full size", icon="FULLSCREEN_ENTER").bl_text_name = self.name

        row.prop_search(self, "loc_vars_code", bpy.data, "texts", text="")
        row.operator('text.get_array_from_text', icon="FILE_REFRESH", text="").origin = self.get_node_origin(props_name=["val_in"])

    def _refresh_inputs(self):
        for i, input in enumerate(reversed(self.inputs)):
            if i in [0] or input.name == "image_in":
                continue
            if not input.is_linked:
                self.inputs.remove(self.inputs[input.name])
        if self.inputs[-1].is_linked:
            new_socket_name = INPUT_NAME_TEMPLATE.format(int(self.inputs[-1].name.split("_")[-1]) + 1)
            self.inputs.new("OCVLMatrixSocket", new_socket_name)

    def _get_context(self):
        context = {"bpy": bpy, "np": np, "cv2": cv2}
        for input in self.inputs:
            if input.is_linked:
                val = input.sv_get()
                if self.is_uuid(val) and val in SOCKET_DATA_CACHE:
                    val = SOCKET_DATA_CACHE[val]
                context.update({input.name: val})
        return context

    @property
    def text_block(self):
        return bpy.data.texts.get(self.loc_vars_code)

    def update_sockets(self, context):
        self.process()
