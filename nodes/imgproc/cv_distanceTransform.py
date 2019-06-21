import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, DISTANCE_TYPE_FOR_TRANSFORM_ITEMS

MASK_SIZE_ITEMS = (
    ("3", "3", "3", "", 0),
    ("5", "5", "5", "", 1),
    ("7", "7", "7", "", 2),
)


class OCVLdistanceTransformNode(OCVLNodeBase):

    n_doc = "Calculates the distance to the closest zero pixel for each pixel of the source image."
    n_quick_link_requirements = {"image_in": {"code_in": "COLOR_BGR2GRAY"}, "image_out": {"width": 300}}
    n_requirements = {"__and__": ["image_in"]}

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()), description="8-bit, single-channel (binary) source image.")
    distanceType_in: bpy.props.EnumProperty(items=DISTANCE_TYPE_FOR_TRANSFORM_ITEMS, default='DIST_L2', update=update_node, description="Type of distance. It can be CV_DIST_L1, CV_DIST_L2 , or CV_DIST_C.")
    maskSize_in: bpy.props.EnumProperty(items=MASK_SIZE_ITEMS, default='3', update=update_node, description="Size of the distance transform mask.")

    image_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()), description="Output image with calculated distances.")

    def init(self, context):
        self.inputs.new("ImageSocket", "image_in")
        self.outputs.new("ImageSocket", "image_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("image_in"),
            'distanceType_in': self.get_from_props("distanceType_in"),
            'maskSize_in': int(self.get_from_props("maskSize_in")),
            }

        image_out = self.process_cv(fn=cv2.distanceTransform, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "distanceType_in")
        self.add_button(layout, "maskSize_in")
