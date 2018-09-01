import bpy
import cv2
import uuid
import random
import numpy as np
from logging import getLogger
from bpy.props import EnumProperty, StringProperty, IntProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode, convert_to_cv_image, updateNode
from ...auth import ocvl_auth
from ... import globals as ocvl

logger = getLogger(__name__)


STREAM_MODE_ITEMS = [
    ("CAMERA", "CAMERA", "Local camera", "", 0),
    ("RTSP", "RTSP", "RTSP/RTP", "", 1),
    ("FILE", "FILE", "File movie", "", 2),
    ]


CAMERA_DEVICE_ITEMS = [
    ("0", "0", "0", "", 0),
    ("1", "1", "1", "", 1),
    ("2", "2", "2", "", 2),
    ("3", "3", "3", "", 3),
]


def reconnect_camera_device(config=0):
    # cap = cv2.VideoCapture("rtsp://admin:12345@192.168.0.4:554")
    ocvl.CAMERA_DEVICE_DICT[config] = cv2.VideoCapture(config)


class OCVLVideoSampleNode(OCVLPreviewNode):
    ''' Video sample '''
    bl_icon = 'IMAGE_DATA'

    def update_layout(self, context):
        logger.debug("UPDATE_LAYOUT")
        self.update_sockets(context)
        updateNode(self, context)

    def update_prop_search(self, context):
        logger.debug("UPDATE_PROP_SEARCH")
        self.process()
        updateNode(self, context)

    width_in = IntProperty(default=100, min=1, max=1024, update=updateNode, name="width_in")
    height_in = IntProperty(default=100, min=1, max=1020, update=updateNode, name="height_in")
    image_out = StringProperty(default=str(uuid.uuid4()))

    loc_stream = StringProperty(default='0', update=updateNode)
    loc_name_image = StringProperty(default='', update=update_prop_search)
    loc_filepath = StringProperty(default='', update=updateNode)
    loc_image_mode = EnumProperty(items=STREAM_MODE_ITEMS, default="CAMERA", update=update_layout)
    loc_camera_device = EnumProperty(items=CAMERA_DEVICE_ITEMS, default="0", update=update_layout)

    def sv_init(self, context):
        self.width = 200
        self.outputs.new('StringsSocket', 'image_out')
        self.update_layout(context)

    def wrapped_process(self):
        logger.info("Process: self: {}, loc_image_mode: {}, loc_filepath: {}".format(self, self.loc_image_mode, self.loc_filepath))
        image = None
        uuid_ = None

        loc_camera_device = int(self.get_from_props("loc_camera_device"))

        if not ocvl.CAMERA_DEVICE_DICT.get(loc_camera_device):
            reconnect_camera_device(loc_camera_device)

        if ocvl.CAMERA_DEVICE_DICT.get(loc_camera_device) and ocvl.CAMERA_DEVICE_DICT.get(loc_camera_device).isOpened():
            _, image = ocvl.CAMERA_DEVICE_DICT.get(loc_camera_device).read()

        if not ocvl.CAMERA_DEVICE_DICT.get(loc_camera_device) or image is None:
            # reconnect_camera_device()
            image = np.zeros((200, 200, 3), np.uint8)

        image, self.image_out = self._update_node_cache(image=image, resize=False, uuid_=uuid_)

        self.outputs['image_out'].sv_set(self.image_out)
        self.make_textures(image, uuid_=self.image_out)

    def _update_node_cache(self, image=None, resize=False, uuid_=None):
        old_image_out = self.image_out
        self.socket_data_cache.pop(old_image_out, None)
        uuid_ = uuid_ if uuid_ else str(uuid.uuid4())
        self.socket_data_cache[uuid_] = image
        return image, uuid_

    def draw_buttons(self, context, layout):
        origin = self.get_node_origin()
        screen = context.screen
        rd = context.scene.render
        self.add_button(layout, "loc_image_mode", expand=True)
        self.add_button(layout, "loc_camera_device", expand=True)
        row = layout.row()
        sub = row.column(align=True)
        sub.menu("RENDER_MT_framerate_presets", text="Framerate")
        sub.prop(rd, "fps")

        if self.loc_image_mode in ["CAMERA", "RTSP"]:
            self.add_button(layout, "loc_stream")
        elif self.loc_image_mode == "FILE":
            col = layout.row().column()
            col_split = col.split(1, align=True)
            col_split.operator('image.image_importer', text='', icon="FILE_FOLDER").origin = origin

        if self.n_id not in self.texture:
            return

        col = layout.row().column()
        col_split = col.split(1, align=True)
        if not screen.is_animation_playing:
            col_split.operator("screen.animation_play", text="", icon='PLAY')
        else:
            col_split.operator("screen.animation_play", text="", icon='PAUSE')

        location_y = -80 if self.loc_image_mode in ["PLANE", "RANDOM"] else -100
        self.draw_preview(layout=layout, prop_name="image_out", location_x=10, location_y=location_y)

    def copy(self, node):
        self.n_id = ''
        self.process()
        node.process()

    def free(self):
        super().free()
        loc_camera_device = int(self.get_from_props("loc_camera_device"))
        if ocvl.CAMERA_DEVICE_DICT.get(loc_camera_device).isOpened():
            ocvl.CAMERA_DEVICE_DICT.get(loc_camera_device).release()

    def update_sockets(self, context):
        self.process()


# if ocvl_auth.ocvl_pro_version_auth:
#     from ...extend.laboratory.ta_image_sample import OCVLImageSampleNode


def register():
    cv_register_class(OCVLVideoSampleNode)


def unregister():
    cv_unregister_class(OCVLVideoSampleNode)

