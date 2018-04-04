import cv2
import uuid
from bpy.props import StringProperty, IntVectorProperty, FloatProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLgetRotationMatrix2DNode(OCVLNode):

    map_matrix_out = StringProperty(name="map_matrix", default=str(uuid.uuid4()))

    center_in = IntVectorProperty(default=(2, 2), min=1, max=30, size=2, update=updateNode,
        description='Center of the rotation in the source image.')
    angle_in = FloatProperty(default=45, min=0, max=360, step=10, update=updateNode,
        description="Rotation angle in degrees.")
    scale_in = FloatProperty(default=1, min=0, max=10, update=updateNode,
        description="Isotropic scale factor.")

    def sv_init(self, context):
        self.width = 180
        self.inputs.new("StringsSocket", "center_in").prop_name = "center_in"
        self.inputs.new("StringsSocket", "angle_in").prop_name = "angle_in"
        self.inputs.new("StringsSocket", "scale_in").prop_name = "scale_in"

        self.outputs.new("StringsSocket", "map_matrix_out")

    def wrapped_process(self):
        kwargs = {
            'center_in': self.get_from_props("center_in"),
            'angle_in': self.get_from_props("angle_in"),
            'scale_in': self.get_from_props("scale_in"),
            }

        map_matrix_out = self.process_cv(fn=cv2.getRotationMatrix2D, kwargs=kwargs)
        self.refresh_output_socket("map_matrix_out", map_matrix_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLgetRotationMatrix2DNode)


def unregister():
    cv_unregister_class(OCVLgetRotationMatrix2DNode)
