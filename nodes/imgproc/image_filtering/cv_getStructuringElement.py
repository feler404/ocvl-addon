import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, BORDER_TYPE_ITEMS

class OCVLgetStructuringElementNode(OCVLNodeBase):
    n_doc = "The function constructs and returns the structuring element that can be further passed to erode(), dilate() or morphologyEx() . But you can also construct an arbitrary binary mask yourself and use it as the structuring element."
    n_note = "When using OpenCV 1.x C API, the created structuring element IplConvKernel* element must be released in the end using cvReleaseStructuringElement(&element)."
    n_requirments = {}

    def set_ksize(self, value):
        if value % 2 == 0:
            value = value + 1
        self["ksize_in"] = value

    def get_ksize(self):
        return self.get("ksize_in", 5)

    shape_in: bpy.props.EnumProperty()#Co tu wwpisać do nawiasu?
    anchor_in: bpy.props.IntVectorProperty(default=(-1, -1), update=update_node, size=2, description="Position of the anchor within the element.")
    ksize_in: bpy.props.IntProperty(default=5, update=update_node, min=1, max=30, get=get_ksize, set=set_ksize,description="Size of the structuring element.")

    def init(self, context):
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('StringsSocket', "anchor_in").prop_name = 'anchor_in'

        self.outputs.new("ImageSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'ksize_in': self.get_from_props("ksize_in"),
            'anchor_in': self.get_from_props("anchor_in")
        }

        retval_out = self.process_cv(fn=cv2.getStructuringElement, kwargs=kwargs)
        self.refresh_output_socket("retval_output", retval_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')
        self.add_button(layout, 'borderType_in')