import cv2
import uuid
from bpy.props import EnumProperty, StringProperty, IntVectorProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, DEVELOP_STATE_ALPHA


M1TYPE_ITEMS = (
    ("CV_32FC1", "CV_32FC1", "CV_32FC1", "", 0),
    ("CV_16SC2", "CV_16SC2", "CV_16SC2", "", 1),
)

class OCVLinitUndistortRectifyMapNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_ALPHA

    cameraMatrix_in = StringProperty(name="cameraMatrix_in", default=str(uuid.uuid4()))
    distCoeffs_in = StringProperty(name="distCoeffs_in", default=str(uuid.uuid4()))
    newCameraMatrix = StringProperty(name="newCameraMatrix", default=str(uuid.uuid4()))
    R_in = StringProperty(name="R_in", default=str(uuid.uuid4()))
    size_in = IntVectorProperty(default=(100, 100), min=1, max=2048, size=2, update=updateNode,
        description='Camera view image size in pixels.')
    m1type_in = EnumProperty(items=M1TYPE_ITEMS, default="CV_32FC1", update=updateNode,
        description="Type of the first output map that can be CV_32FC1 or CV_16SC2.")

    map1_out = StringProperty(name="map1_out", default=str(uuid.uuid4()))
    map2_out = StringProperty(name="map2_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "cameraMatrix_in")
        self.inputs.new("StringsSocket", "distCoeffs_in")
        self.inputs.new("StringsSocket", "newCameraMatrix")
        self.inputs.new("StringsSocket", "R_in")
        self.inputs.new("StringsSocket", "size_in").prop_name = "size_in"

        self.outputs.new("StringsSocket", "map1_out")
        self.outputs.new("StringsSocket", "map2_out")

    def wrapped_process(self):
        self.check_input_requirements(["cameraMatrix_in", "distCoeffs_in", "newCameraMatrix", "R_in"])

        kwargs = {
            'cameraMatrix_in': self.get_from_props("cameraMatrix_in"),
            'newCameraMatrix': self.get_from_props("newCameraMatrix"),
            'distCoeffs_in': self.get_from_props("distCoeffs_in"),
            'R_in': self.get_from_props("R_in"),
            'size_in': self.get_from_props("size_in"),
            'm1type_in': self.get_from_props("m1type_in"),
            }

        map1_out, map2_out = self.process_cv(fn=cv2.initUndistortRectifyMap, kwargs=kwargs)
        self.refresh_output_socket("map1_out", map1_out, is_uuid_type=True)
        self.refresh_output_socket("map2_out", map2_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "m1type_in", expand=True)


def register():
    cv_register_class(OCVLinitUndistortRectifyMapNode)


def unregister():
    cv_unregister_class(OCVLinitUndistortRectifyMapNode)
