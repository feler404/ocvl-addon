import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, COLOR_DEPTH_WITH_NONE_ITEMS




class OCVLwatershedNode(OCVLNode):

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()), description="Input 8-bit 3-channel image.")
    markers_in = StringProperty(name="markers_in", default=str(uuid.uuid4()), description="Input/output 32-bit single-channel image (map) of markers. It should have the same size as image.")

    markers_out = StringProperty(name="markers_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "markers_in")

        self.outputs.new("StringsSocket", "markers_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'markers_in': self.get_from_props("markers_in"),
            }

        markers_out = self.process_cv(fn=cv2.watershed, kwargs=kwargs)
        self.refresh_output_socket("markers_out", markers_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLwatershedNode)


def unregister():
    cv_unregister_class(OCVLwatershedNode)
