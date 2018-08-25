import bpy
import cv2
import uuid
import random
import numpy as np
from logging import getLogger
from bpy.props import EnumProperty, StringProperty, IntProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode, convert_to_cv_image, updateNode
from ...auth import ocvl_auth

logger = getLogger(__name__)

IMAGE_MODE_ITEMS = [
    ("FILE", "FILE", "From file", "", 0),
    ("PLANE", "PLANE", "Plane color", "", 1),
    ("RANDOM", "RANDOM", "Random figures", "", 2),
    ]


def connect_rtsp():
    cap = cv2.VideoCapture("rtsp://admin:12345@192.168.0.4:554")
    np.cap = cap


connect_rtsp()


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

    rtsp_in = StringProperty(default="")

    width_in = IntProperty(default=100, min=1, max=1024, update=updateNode, name="width_in")
    height_in = IntProperty(default=100, min=1, max=1020, update=updateNode, name="height_in")
    width_out = IntProperty(default=0, name="width_out")
    height_out = IntProperty(default=0, name="height_out")
    image_out = StringProperty(default=str(uuid.uuid4()))

    loc_name_image = StringProperty(default='', update=update_prop_search)
    loc_filepath = StringProperty(default='', update=updateNode)
    loc_image_mode = EnumProperty(items=IMAGE_MODE_ITEMS, default="RANDOM", update=update_layout)

    def sv_init(self, context):
        self.inputs.new('StringsSocket', 'rtsp_in').prop_name= "rtsp_in"
        self.width = 200
        self.outputs.new('StringsSocket', 'image_out')
        self.outputs.new('StringsSocket', 'width_out')
        self.outputs.new('StringsSocket', 'height_out')
        self.update_layout(context)

    def wrapped_process(self):
        logger.info("Process: self: {}, loc_image_mode: {}, loc_filepath: {}".format(self, self.loc_image_mode, self.loc_filepath))
        image = None
        uuid_ = None
        print (2222, "connect", np.cap.isOpened())


        _, image = np.cap.read()


        # for i in range(30):
        #     if not np.cap.grab():
        #         break

        if image is None:
            np.cap.release()
            connect_rtsp()
            image = np.zeros((200, 200, 3), np.uint8)

        print(11111, image.shape)
        image, self.image_out = self._update_node_cache(image=image, resize=False, uuid_=uuid_)

        self.outputs['image_out'].sv_set(self.image_out)
        self.refresh_output_socket("height_out", image.shape[0])
        self.refresh_output_socket("width_out", image.shape[1])
        self.make_textures(image, uuid_=self.image_out)

    def _update_node_cache(self, image=None, resize=False, uuid_=None):
        old_image_out = self.image_out
        self.socket_data_cache.pop(old_image_out, None)
        uuid_ = uuid_ if uuid_ else str(uuid.uuid4())
        self.socket_data_cache[uuid_] = image
        return image, uuid_

    def draw_buttons(self, context, layout):
        origin = self.get_node_origin()
        self.add_button(layout, "loc_image_mode", expand=True)

        if self.loc_image_mode == "FILE":
            col = layout.row().column()
            col_split = col.split(1, align=True)
            col_split.operator('image.image_importer', text='', icon="FILE_FOLDER").origin = origin
        elif self.loc_image_mode == "PLANE":
            pass
        elif self.loc_image_mode == "RANDOM":
            pass

        if self.n_id not in self.texture:
            return

        location_y = -20 if self.loc_image_mode in ["PLANE", "RANDOM"] else -40
        self.draw_preview(layout=layout, prop_name="image_out", location_x=10, location_y=location_y)

        col = layout.row().column()
        col_split = col.split(1, align=True)
        col_split.operator('wm.modal_timer_refresh_rtsp_image_operator', text="RTSP start", icon='PARTICLES')

    def copy(self, node):
        self.n_id = ''
        self.process()
        node.process()

    def update_sockets(self, context):
        self.process()


# if ocvl_auth.ocvl_pro_version_auth:
#     from ...extend.laboratory.ta_image_sample import OCVLImageSampleNode


def register():
    cv_register_class(OCVLVideoSampleNode)


def unregister():
    cv_unregister_class(OCVLVideoSampleNode)

