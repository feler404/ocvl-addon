import cv2
import uuid
from bpy.props import StringProperty, IntProperty

from ...utils import cv_register_class, cv_unregister_class, updateNode, OCVLNode


class OCVLpyrDownNode(OCVLNode):

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))

    image_0_out = StringProperty(name="image_0_out", default=str(uuid.uuid4()))
    image_1_out = StringProperty(name="image_1_out", default=str(uuid.uuid4()))
    image_2_out = StringProperty(name="image_2_out", default=str(uuid.uuid4()))
    image_3_out = StringProperty(name="image_3_out", default=str(uuid.uuid4()))
    image_4_out = StringProperty(name="image_4_out", default=str(uuid.uuid4()))
    image_5_out = StringProperty(name="image_5_out", default=str(uuid.uuid4()))
    image_6_out = StringProperty(name="image_6_out", default=str(uuid.uuid4()))
    image_7_out = StringProperty(name="image_7_out", default=str(uuid.uuid4()))
    image_8_out = StringProperty(name="image_8_out", default=str(uuid.uuid4()))
    image_9_out = StringProperty(name="image_9_out", default=str(uuid.uuid4()))
    image_full_out = StringProperty(name="image_full_out", default=str(uuid.uuid4()))

    loc_pyramid_size = IntProperty(default=3, min=1, max=10, update=updateNode,
        description='Number levels of pyramids.')

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "loc_pyramid_size").prop_name = 'loc_pyramid_size'

        self.outputs.new("StringsSocket", "image_full_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        image_in = self.get_from_props("image_in")
        loc_pyramid_size = self.get_from_props("loc_pyramid_size")

        img = image_in.copy()
        pyramid = [image_in]
        for i in range(loc_pyramid_size):
            img = cv2.pyrDown(img)
            pyramid.append(img)
        self._update_sockets(pyramid)
        self.refresh_output_socket("image_full_out", pyramid, is_uuid_type=True)

    def _update_sockets(self, pyramid):
        for i in range(10):
            prop_name = "image_{}_out".format(i)

            if i < len(pyramid):
                _uuid = str(uuid.uuid4())
                if self.outputs.get(prop_name):
                    pass
                else:
                    self.outputs.new("StringsSocket", prop_name)
                setattr(self, prop_name, _uuid)
                self.socket_data_cache[_uuid] = pyramid[i]
                self.outputs[prop_name].sv_set(_uuid)
            else:
                if self.outputs.get(prop_name):
                    self.outputs.remove(self.outputs[prop_name])

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLpyrDownNode)


def unregister():
    cv_unregister_class(OCVLpyrDownNode)
