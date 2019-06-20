import uuid

import bpy
import cv2
import numpy as np
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLdilateNode(OCVLNodeBase):

    bl_icon = 'FILTER'
    n_doc = "Dilates an image by using a specific structuring element."

    def get_anchor(self):
        return self.get("anchor_in", (-1, -1))

    def set_anchor(self, value):
        anchor_x = value[0] if -1 <= value[0] < self.ksize_in[0] else self.anchor_in[0]
        anchor_y = value[1] if -1 <= value[1] < self.ksize_in[1] else self.anchor_in[1]
        self["anchor_in"] = (anchor_x, anchor_y)

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()), description="Input image.")
    image_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()), description="Output image.")

    ksize_in: bpy.props.IntVectorProperty(default=(3, 3), update=update_node, min=1, max=30, size=2, description="Structuring element used for erosion.")
    anchor_in: bpy.props.IntVectorProperty(default=(-1, -1), update=update_node, get=get_anchor, set=set_anchor, size=2, description="Position of the anchor within the element.")
    iterations_in: bpy.props.IntProperty(default=2, min=1, max=10, update=update_node, description="Number of times erosion is applied.")

    def init(self, context):
        self.width = 150
        self.inputs.new("ImageSocket", "image_in")
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('StringsSocket', "anchor_in").prop_name = 'anchor_in'
        self.inputs.new('StringsSocket', "iterations_in").prop_name = 'iterations_in'

        self.outputs.new("ImageSocket", "image_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kernel = np.array(self.get_from_props("ksize_in"))
        kwargs = {
            'src': self.get_from_props("image_in"),
            'kernel': kernel,
            'anchor_in': self.get_from_props("anchor_in"),
            'iterations_in': self.get_from_props("iterations_in"),
            }

        image_out = self.process_cv(fn=cv2.dilate, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass
