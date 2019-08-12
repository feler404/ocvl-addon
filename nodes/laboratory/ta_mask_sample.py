import bpy
import cv2
import uuid
import random
import numpy as np
from logging import getLogger

from ocvl.core.node_base import OCVLPreviewNodeBase
from ocvl.core.constants import NP_VALUE_TYPE_ITEMS

logger = getLogger(__name__)


IMAGE_MODE_ITEMS = [
    ("PLANE", "PLANE", "Plane color", "", 0),
    ("RANDOM", "RANDOM", "Random figures", "", 1),
    ]


PROPS_MAPS = {
    IMAGE_MODE_ITEMS[0][0]: ("width_in", "height_in"),
    IMAGE_MODE_ITEMS[1][0]: ("width_in", "height_in"),
}


class OCVLMaskSampleNode(OCVLPreviewNodeBase):
    bl_icon = 'IMAGE_DATA'

    n_doc = "Create new image mask."
    n_requirements = {}

    def update_layout(self, context):
        self.update_sockets(context)
        self.process()

    def update_prop_search(self, context):
        self.update_sockets(context)
        self.process()

    width_in: bpy.props.IntProperty(default=100, min=1, max=1024, update=update_layout, name="width_in")
    height_in: bpy.props.IntProperty(default=100, min=1, max=1024, update=update_layout, name="height_in")
    value_type_in: bpy.props.EnumProperty(items=NP_VALUE_TYPE_ITEMS, default='uint8', update=update_layout, description="Data type.")

    width_out: bpy.props.IntProperty(default=0, name="width_out")
    height_out: bpy.props.IntProperty(default=0, name="height_out")
    image_out: bpy.props.StringProperty(default=str(uuid.uuid4()))

    loc_image_mode: bpy.props.EnumProperty(items=IMAGE_MODE_ITEMS, default="RANDOM", update=update_layout)
    loc_resize: bpy.props.BoolProperty(default=False, name="Resize", update=update_layout)

    def init(self, context):
        self.width = 200

        self.outputs.new('OCVLMaskSocket', 'image_out')
        self.outputs.new('OCVLMatrixSocket', 'width_out')
        self.outputs.new('OCVLMatrixSocket', 'height_out')

        self.update_layout(context)

    def wrapped_process(self):
        image = None
        uuid_ = None
        value_type_in = self.get_from_props("value_type_in")

        if self.loc_image_mode in ["PLANE", "RANDOM"]:
            width_in = self.get_from_props("width_in")
            height_in = self.get_from_props("height_in")
            image = np.zeros((width_in, height_in, 3), np.uint8)
            image[:,:,] = (0, 0, 0)
            if self.loc_image_mode == "RANDOM":
                for i in range(5):
                    pt1 = (random.randint(1, width_in), random.randint(1, height_in))
                    pt2 = (random.randint(1, width_in), random.randint(1, height_in))
                    image = cv2.line(image, pt1, pt2, (255, 255, 255), random.randint(1, 10))

        image = cv2.cvtColor(src=image, code=cv2.COLOR_RGB2GRAY)
        if value_type_in != "NONE":
            image = image.astype(getattr(np, value_type_in))

        image, self.image_out = self._update_node_cache(image=image, resize=False, uuid_=uuid_)
        self.outputs['image_out'].sv_set(self.image_out)
        self.refresh_output_socket("height_out", image.shape[0])
        self.refresh_output_socket("width_out", image.shape[1])
        self.make_textures(image, uuid_=self.image_out)
        self._add_meta_info(image)

    def _update_node_cache(self, image=None, resize=False, uuid_=None):
        old_image_out = self.image_out
        self.socket_data_cache.pop(old_image_out, None)
        uuid_ = uuid_ if uuid_ else str(uuid.uuid4())
        self.socket_data_cache[uuid_] = image
        return image, uuid_

    def _add_meta_info(self, image):
        self.n_meta = "\n".join(["Width: {}".format(image.shape[1]),
                                 "Height: {}".format(image.shape[0]),
                                 "Channels: {}".format(1 if len(image.shape) > 1 else image.shape[2]),
                                 "DType: {}".format(image.dtype),
                                 "Size: {}".format(image.size)])

    def draw_buttons(self, context, layout):
        origin = self.get_node_origin()
        self.add_button(layout, "value_type_in", expand=True)
        self.add_button(layout, "loc_image_mode", expand=True)

        if self.loc_image_mode == "PLANE":
            pass
        elif self.loc_image_mode == "RANDOM":
            pass

        if self.n_id not in self.texture:
            return

        location_y = -150 if self.loc_image_mode in ["PLANE", "RANDOM"] else -170
        self.draw_preview(layout=layout, prop_name="image_out", location_x=10, location_y=location_y)

    def update_sockets(self, context):
        self.update_sockets_for_node_mode(PROPS_MAPS, self.loc_image_mode)
