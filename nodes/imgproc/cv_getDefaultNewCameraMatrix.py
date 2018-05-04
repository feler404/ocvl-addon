import cv2
import uuid
from gettext import gettext as _
from bpy.props import StringProperty, IntVectorProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode, DEVELOP_STATE_BETA


class OCVLgetDefaultNewCameraMatrixNode(OCVLNode):
    bl_develop_state = DEVELOP_STATE_BETA

    _doc = _("Returns the default new camera matrix.")

    cameraMatrix_in = StringProperty(name="cameraMatrix_in", default=str(uuid.uuid4()),
        description=_("Input camera matrix."))
    imgsize_in = IntVectorProperty(default=(100, 100), min=1, max=2048, size=2, update=updateNode,
        description=_("Camera view image size in pixels."))
    centerPrincipalPoint_in = BoolProperty(default=False, update=updateNode,
        description=_("Location of the principal point in the new camera matrix. The parameter indicates whether this location should be at the image center or not."))

    retval_out = StringProperty(name="retval_out", default=str(uuid.uuid4()))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "cameraMatrix_in")
        self.inputs.new("StringsSocket", "imgsize_in").prop_name = "imgsize_in"

        self.outputs.new("StringsSocket", "retval_out")

    def wrapped_process(self):
        self.check_input_requirements(["cameraMatrix_in"])

        kwargs = {
            'cameraMatrix_in': self.get_from_props("cameraMatrix_in"),
            'imgsize_in': self.get_from_props("imgsize_in"),
            'centerPrincipalPoint_in': self.get_from_props("centerPrincipalPoint_in"),
            }

        retval_out = self.process_cv(fn=cv2.getDefaultNewCameraMatrix, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'centerPrincipalPoint_in')


def register():
    cv_register_class(OCVLgetDefaultNewCameraMatrixNode)


def unregister():
    cv_unregister_class(OCVLgetDefaultNewCameraMatrixNode)
