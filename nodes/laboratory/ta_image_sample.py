import bpy
import cv2
import uuid
import random
import numpy as np
from logging import getLogger

from ocvl.core.node_base import OCVLPreviewNodeBase
from ocvl.core.image_utils import convert_to_cv_image
from ocvl.core.constants import NP_VALUE_TYPE_ITEMS

logger = getLogger(__name__)


CODE_COLOR_POOR_ITEMS_FOR_IMAGE_SAMPLE = (
    ("NONE", "NONE", "NONE", "", 0),
    ("COLOR_BGR2GRAY", "COLOR_BGR2GRAY", "COLOR_BGR2GRAY", "", 1),
    ("COLOR_BGR2RGB", "COLOR_BGR2RGB", "COLOR_BGR2RGB", "", 2),
    ("COLOR_BGR2HLS", "COLOR_BGR2HLS", "COLOR_BGR2HLS", "", 3),
    ("COLOR_BGR2HSV", "COLOR_BGR2HSV", "COLOR_BGR2HSV", "", 4),
    ("COLOR_BGR2LAB", "COLOR_BGR2LAB", "COLOR_BGR2LAB", "", 5),
    ("COLOR_BGR2LUV", "COLOR_BGR2LUV", "COLOR_BGR2LUV", "", 6),
    ("COLOR_BGR2YCR_CB", "COLOR_BGR2YCR_CB", "COLOR_BGR2YCR_CB", "", 7),
    ("COLOR_BGR2YUV", "COLOR_BGR2YUV", "COLOR_BGR2YUV", "", 8),
)


IMAGE_MODE_ITEMS = [
    # ("CAM", "CAM", "From camera", "", 0),
    ("FILE", "FILE", "From file", "", 0),
    ("PLANE", "PLANE", "Plane color", "", 1),
    ("RANDOM", "RANDOM", "Random figures", "", 2),
    ]


PROPS_MAPS = {
    # IMAGE_MODE_ITEMS[0][0]: ("width_in", "height_in"),
    IMAGE_MODE_ITEMS[0][0]: ("width_in", "height_in"),
    IMAGE_MODE_ITEMS[1][0]: ("color_in", "width_in", "height_in"),
    IMAGE_MODE_ITEMS[2][0]: ("color_in", "width_in", "height_in"),
}



class OCVLImageSampleNode(OCVLPreviewNodeBase):
    bl_icon = 'IMAGE_DATA'

    n_doc = "Create new image/matrix."
    n_requirements = {}

    def update_layout(self, context):
        self.update_sockets(context)
        self.process()

    def update_prop_search(self, context):
        self.update_sockets(context)
        self.process()

    width_in: bpy.props.IntProperty(default=100, min=1, max=1024, update=update_layout, name="width_in")
    height_in: bpy.props.IntProperty(default=100, min=1, max=1024, update=update_layout, name="height_in")
    color_in: bpy.props.FloatVectorProperty(update=update_layout, name='color_in', default=(.3, .3, .2, 1.0), size=4, min=0.0, max=1.0, subtype='COLOR')
    code_in: bpy.props.EnumProperty(items=CODE_COLOR_POOR_ITEMS_FOR_IMAGE_SAMPLE, default='NONE', update=update_layout, description="Color space conversion code (see cv::ColorConversionCodes).")
    value_type_in: bpy.props.EnumProperty(items=NP_VALUE_TYPE_ITEMS, default='uint8', update=update_layout, description="Data type.")

    width_out: bpy.props.IntProperty(default=0, name="width_out")
    height_out: bpy.props.IntProperty(default=0, name="height_out")
    image_out: bpy.props.StringProperty(default=str(uuid.uuid4()))

    loc_name_image: bpy.props.StringProperty(default='', update=update_prop_search)
    loc_filepath: bpy.props.StringProperty(default='', update=update_layout)
    loc_image_mode: bpy.props.EnumProperty(items=IMAGE_MODE_ITEMS, default="RANDOM", update=update_layout)
    loc_resize: bpy.props.BoolProperty(default=False, name="Resize", update=update_layout)

    def init(self, context):
        self.width = 200
        self.inputs.new('OCVLColorSocket', 'color_in').prop_name = 'color_in'

        self.outputs.new('OCVLImageSocket', 'image_out')
        self.outputs.new('OCVLObjectSocket', 'width_out')
        self.outputs.new('OCVLObjectSocket', 'height_out')

        self.update_layout(context)

    def wrapped_process(self):
        logger.info("Process: self: {}, loc_image_mode: {}, loc_filepath: {}".format(self, self.loc_image_mode, self.loc_filepath))
        image = None
        uuid_ = None
        code_in = self.get_from_props("code_in")
        value_type_in = self.get_from_props("value_type_in")

        if self.loc_image_mode in ["PLANE", "RANDOM"]:
            color_in = self.get_from_props("color_in")
            width_in = self.get_from_props("width_in")
            height_in = self.get_from_props("height_in")
            image = np.zeros((height_in, width_in, 3), np.uint8)
            image[:,:,] = color_in
            if self.loc_image_mode == "RANDOM":
                for i in range(20):
                    pt1 = (random.randint(1, height_in), random.randint(1, width_in))
                    pt2 = (random.randint(1, height_in), random.randint(1, width_in))
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    image = cv2.line(image, pt1, pt2, color, random.randint(1, 10))
        elif self.loc_image_mode == "FILE":
            if self.loc_name_image in bpy.data.images:
                image = convert_to_cv_image(bpy.data.images[self.loc_name_image])
                uuid_ = self.loc_name_image
            elif self.loc_filepath:
                image = cv2.imread(self.loc_filepath, flags=cv2.IMREAD_UNCHANGED)
            if image is None:
                image = np.zeros((200, 200, 3), np.uint8)

        if code_in != "NONE":
            image = cv2.cvtColor(src=image, code=code_in)

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
        self.add_button(layout, "loc_image_mode", expand=True)
        self.add_button(layout, "code_in")
        self.add_button(layout, "value_type_in")

        if self.loc_image_mode == "FILE":
            col = layout.row().column()
            col_split = col.split(factor=1, align=True)
            col_split.operator('ocvl.ocvl_image_importer', text='', icon="FILE_FOLDER").origin = origin
        elif self.loc_image_mode == "PLANE":
            pass
        elif self.loc_image_mode == "RANDOM":
            pass

        if self.n_id not in self.texture:
            return

        location_y = -180 if self.loc_image_mode in ["PLANE", "RANDOM"] else -200
        self.draw_preview(layout=layout, prop_name="image_out", location_x=10, location_y=location_y)

    def update_sockets(self, context):
        self.update_sockets_for_node_mode(PROPS_MAPS, self.loc_image_mode)
        if self.loc_image_mode in ["FILE", "CAM"] and not self.loc_resize:
            if "width_in" in self.inputs:
                self.inputs.remove(self.inputs["width_in"])
            if "height_in" in self.inputs:
                self.inputs.remove(self.inputs["height_in"])
