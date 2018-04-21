import cv2
import uuid
import numpy as np
from gettext import gettext as _
from bpy.props import StringProperty

from ...extend.utils import cv_register_class, cv_unregister_class, OCVLNode


MODE_ITEMS = [
    ("EMPTY", "EMPTY", "EMPTY", "", 0),
    ("FULL", "FULL", "FULL", "", 1),
    ]


PROPS_MAPS = {
    MODE_ITEMS[0][0]: (),
    MODE_ITEMS[1][0]: ("layer_0_in", "layer_1_in", "layer_2_in"),
}


class OCVLmergeNode(OCVLNode):

    _doc = _("Creates one multichannel array out of several single-channel ones.")
    _note= _("In example image was used node cvtColor to make one single channel array in graz scale. Node merge is giving out multichannel array on the input channel Red.")

    layer_0_in = StringProperty(name="layer_0_in", default=str(uuid.uuid4()),
        description=_("First channel Blue."))
    layer_1_in = StringProperty(name="layer_1_in", default=str(uuid.uuid4()),
        description=_("Second channel Green."))
    layer_2_in = StringProperty(name="layer_2_in", default=str(uuid.uuid4()),
        description=_("Third channel Red."))
    # layer_3_in = StringProperty(name="layer_3_in", default=str(uuid.uuid4()))

    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Image output."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "layer_0_in")
        self.inputs.new("StringsSocket", "layer_1_in")
        self.inputs.new("StringsSocket", "layer_2_in")
        # self.inputs.new("StringsSocket", "layer_3_in")

        self.outputs.new("StringsSocket", "image_out")

    def wrapped_process(self):
        mv_tmp = []
        mv = []
        widht = hight = None
        for layer_name in PROPS_MAPS["FULL"]:
            layer = self.get_from_props(layer_name)
            if type(layer) not in (str, type(None)):
                widht, hight = layer.shape
                dtype = layer.dtype
            else:
                layer = None
            mv_tmp.append(layer)

        if not widht:
            return

        for layer in mv_tmp:
            if layer is None:
                layer = np.zeros((widht, hight), dtype=dtype)
            mv.append(layer)

        kwargs = {
            'mv': mv,
            }

        image_out = self.process_cv(fn=cv2.merge, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        pass


def register():
    cv_register_class(OCVLmergeNode)


def unregister():
    cv_unregister_class(OCVLmergeNode)
