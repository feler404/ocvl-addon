import cv2
import uuid
from bpy.props import StringProperty, IntProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLgetRectSubPixNode(OCVLNode):

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()))
    patch_out = StringProperty(name="patch_out", default=str(uuid.uuid4()))

    patchSize_in = IntVectorProperty(default=(5, 5), min=1, max=30, size=2, update=updateNode,
        description='Size of the extracted patch.')
    center_in = IntVectorProperty(default=(2, 2), min=1, max=30, size=2, update=updateNode,
        description='Floating point coordinates of the center of the extracted rectangle.')
    patchType_in = IntProperty(default=-1, min=-1, max=30, update=updateNode,
        description="Depth of the extracted pixels. By default, they have the same depth as src.")

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.inputs.new("StringsSocket", "patchSize_in").prop_name = "patchSize_in"
        self.inputs.new("StringsSocket", "center_in").prop_name = "center_in"
        self.inputs.new("StringsSocket", "patchType_in").prop_name = "patchType_in"

        self.outputs.new("StringsSocket", "patch_out")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])

        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'patchSize_in': self.get_from_props("patchSize_in"),
            'center_in': self.get_from_props("center_in"),
            'patchType_in': self.get_from_props("patchType_in"),
            }

        patch_out = self.process_cv(fn=cv2.getRectSubPix, kwargs=kwargs)
        self.refresh_output_socket("patch_out", patch_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLgetRectSubPixNode)


def unregister():
    cv_unregister_class(OCVLgetRectSubPixNode)
