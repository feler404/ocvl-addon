import uuid
from logging import getLogger

import bpy
import cv2
import numpy as np
from ocvl.core.globals import CAMERA_DEVICE_DICT
from ocvl.core.node_base import OCVLPreviewNodeBase, update_node

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
    CAMERA_DEVICE_DICT[config] = cv2.VideoCapture(config)


class OCVLVideoSampleNode(OCVLPreviewNodeBase):
    ''' Video sample '''
    bl_icon = 'IMAGE_DATA'

    n_doc = "Video sample"
    n_requirements = {}
    n_meta = ""

    def update_layout(self, context):
        logger.debug("UPDATE_LAYOUT")
        self.update_sockets(context)
        update_node(self, context)

    def update_prop_search(self, context):
        logger.debug("UPDATE_PROP_SEARCH")
        self.process()
        update_node(self, context)

    width_in: bpy.props.IntProperty(default=100, min=1, max=1024, update=update_node, name="width_in")
    height_in: bpy.props.IntProperty(default=100, min=1, max=1020, update=update_node, name="height_in")
    image_out: bpy.props.StringProperty(default=str(uuid.uuid4()))

    loc_stream: bpy.props.StringProperty(default='0', update=update_node)
    loc_name_image: bpy.props.StringProperty(default='', update=update_prop_search)
    loc_filepath: bpy.props.StringProperty(default='', update=update_node)
    loc_image_mode: bpy.props.EnumProperty(items=STREAM_MODE_ITEMS, default="CAMERA", update=update_layout)
    loc_camera_device: bpy.props.EnumProperty(items=CAMERA_DEVICE_ITEMS, default="0", update=update_layout)

    def init(self, context):
        self.width = 200
        self.outputs.new('OCVLImageSocket', 'image_out')
        self.outputs.new('OCVLObjectSocket', 'width_out')
        self.outputs.new('OCVLObjectSocket', 'height_out')
        self.update_layout(context)

    def wrapped_process(self, *args):
        logger.info("Process: self: {}, loc_image_mode: {}, loc_filepath: {}".format(self, self.loc_image_mode, self.loc_filepath))
        image = None
        uuid_ = None

        current_camera = self._get_current_camera()
        _, image = current_camera.read()

        if not current_camera or image is None:
            # reconnect_camera_device()
            image = np.zeros((200, 200, 3), np.uint8)

        image, self.image_out = self._update_node_cache(image=image, resize=False, uuid_=uuid_)

        self.outputs['image_out'].sv_set(self.image_out)
        self.make_textures(image, uuid_=self.image_out)
        self.process_connected_nodes()

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
            col_split = col.split(factor=1, align=True)
            col_split.operator('ocvl.ocvl_image_importer', text='', icon="FILE_FOLDER").origin = origin

        if self.n_id not in self.texture:
            return

        col = layout.row().column()
        col_split = col.split(factor=1, align=True)
        if not screen.is_animation_playing:
            col_split.operator("screen.animation_play", text="", icon='PLAY')
        else:
            col_split.operator("screen.animation_play", text="", icon='PAUSE')

        location_y = -250
        self.draw_preview(layout=layout, prop_name="image_out", location_x=10, location_y=location_y)

    def free(self):
        super().free()
        self._free_cameras()
        self._free_handlers()

    def _free_cameras(self):
        for camera_device_number in [0, 1, 2, 3]:
            camera_device = CAMERA_DEVICE_DICT.get(camera_device_number)
            if camera_device and camera_device.isOpened():
                camera_device.release()
                CAMERA_DEVICE_DICT.pop(camera_device_number)

    def _free_handlers(self):
        index_handler = None
        for handler in bpy.app.handlers.frame_change_pre:
            if f'"{self.name}"' in str(handler):
                index_handler = bpy.app.handlers.frame_change_pre.index(handler)
        if index_handler:
            bpy.app.handlers.frame_change_pre.pop(index_handler)
        bpy.ops.screen.animation_cancel()

    def _get_current_camera(self):
        self._check_handlers()
        loc_camera_device = int(self.get_from_props("loc_camera_device"))

        if not CAMERA_DEVICE_DICT.get(loc_camera_device):
            reconnect_camera_device(loc_camera_device)
        current_camera = CAMERA_DEVICE_DICT.get(loc_camera_device)
        return current_camera

    def _check_handlers(self):
        if not self.name in str(bpy.app.handlers.frame_change_pre):
            bpy.app.handlers.frame_change_pre.append(self.wrapped_process)

    def update_sockets(self, context):
        self.process()
