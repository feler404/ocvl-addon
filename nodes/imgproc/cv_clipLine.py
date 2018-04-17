import cv2
import uuid
from bpy.props import StringProperty, IntVectorProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


class OCVLclipLineNode(OCVLNode):
    bl_icon = 'GREASEPENCIL'

    imgRect_in = StringProperty(name="imgRect_in", default=str(uuid.uuid4()))
    retval_out = StringProperty(name="retval_out", default=str(uuid.uuid4()))
    pt1_out = StringProperty(name="pt1_out", default=str(uuid.uuid4()))
    pt2_out = StringProperty(name="pt2_out", default=str(uuid.uuid4()))

    pt1_in = IntVectorProperty(default=(0, 0), size=2, min=0, update=updateNode,
        description="First point of the line segment.")
    pt2_in = IntVectorProperty(default=(1, 1), size=2, min=0, update=updateNode,
        description="First point of the line segment.")

    def sv_init(self, context):
        self.width = 200
        self.inputs.new("StringsSocket", "imgRect_in")
        self.inputs.new('StringsSocket', "pt1_in").prop_name = 'pt1_in'
        self.inputs.new('StringsSocket', "pt2_in").prop_name = 'pt2_in'

        self.outputs.new("StringsSocket", "retval_out")
        self.outputs.new("StringsSocket", "pt1_out")
        self.outputs.new("StringsSocket", "pt2_out")

    def wrapped_process(self):
        self.check_input_requirements(["imgRect_in"])

        kwargs = {
            'imgRect_in': self.get_from_props("imgRect_in"),
            'pt1_in': self.get_from_props("pt1_in"),
            'pt2_in': self.get_from_props("pt2_in"),
            }

        retval_out, pt1_out, pt2_out = self.process_cv(fn=cv2.clipLine, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)
        self.refresh_output_socket("pt1_out", pt1_out, is_uuid_type=True)
        self.refresh_output_socket("pt2_out", pt2_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLclipLineNode)


def unregister():
    cv_unregister_class(OCVLclipLineNode)
