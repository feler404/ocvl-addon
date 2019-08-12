import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


SDEPTH_ITEMS = (
    ("MORPH_RECT", "MORPH_RECT", "MORPH_RECT", "", 0),
    ("MORPH_ELLIPSE", "MORPH_ELLIPSE", "MORPH_ELLIPSE", "", 1),
    ("MORPH_CROSS", "MORPH_CROSS", "MORPH_CROSS", "", 2),
    ("CV_SHAPE_CUSTOM", "CV_SHAPE_CUSTOM", "CV_SHAPE_CUSTOM", "", 3))


class OCVLgetStructuringElementNode(OCVLNodeBase):
    n_doc = "Returns a structuring element of the specified size and shape for morphological operations."
    n_note = "When using OpenCV 1.x C API, the created structuring element IplConvKernel* element must be released in the end using cvReleaseStructuringElement(&element)."
    n_requirments = {}

    shape_in: bpy.props.EnumProperty(items=SDEPTH_ITEMS, default="MORPH_RECT", update=update_node)
    ksize_in: bpy.props.IntVectorProperty(default=(3, 3), update=update_node, min=1, max=30, size=2, description="Size of the structuring element.")
    anchor_in: bpy.props.IntVectorProperty(default=(-1, -1), update=update_node, min=-1, max=30, size=2, description="Position of the anchor within the element.")

    retval_out: bpy.props.StringProperty(description="The function constructs and returns the structuring element that can be further passed to erode(), dilate() or morphologyEx() . But you can also construct an arbitrary binary mask yourself and use it as the structuring element.")

    def init(self, context):
        self.width = 200
        self.inputs.new('OCVLMatrixSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('OCVLMatrixSocket', "anchor_in").prop_name = 'anchor_in'

        self.outputs.new("OCVLMatrixSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'ksize_in': self.get_from_props("ksize_in"),
            'anchor_in': self.get_from_props("anchor_in"),
            'shape_in': self.get_from_props("shape_in"),
        }

        retval_out = self.process_cv(fn=cv2.getStructuringElement, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'shape_in')