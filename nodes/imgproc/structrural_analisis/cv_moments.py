import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLmomentsNode(OCVLNodeBase):

    n_doc = "Calculates all of the moments up to the third order of a polygon or rasterized shape."
    n_requirements = {"__and__": ["array_in"]}
    n_quick_link_requirements = {"array_in": {"code_in": "COLOR_BGR2GRAY"}}

    array_in: bpy.props.StringProperty(name="array_in", default=str(uuid.uuid4()), description="Raster image (single-channel, 8-bit or floating-point 2D array) or an array") #pobrane z opisu dla 'array' nie wiem czy dobrze
    binaryarray_in: bpy.props.BoolProperty(default=False, update=update_node, description="If it is true, all non-zero image pixels are treated as 1's. The parameter is used for images only.")

    retval_out: bpy.props.StringProperty(name="retval_out", default=str(uuid.uuid4()), description="Output moments.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "array_in")
        self.outputs.new("OCVLObjectSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'array_in': self.get_from_props("array_in"),
            'binaryImage': self.get_from_props("binaryarray_in"),
            }

        retval_out = self.process_cv(fn=cv2.moments, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'binaryarray_in')
