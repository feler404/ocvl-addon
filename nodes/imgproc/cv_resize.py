import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, IntVectorProperty, FloatProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, INTERPOLATION_ITEMS, updateNode


RESIZE_MODE_ITEMS = [
    ("SIZE", "SIZE", "SIZE", "", 0),
    ("FACTOR", "FACTOR", "FACTOR", "", 1),
    ]


PROPS_MAPS = {
    RESIZE_MODE_ITEMS[0][0]: ("dsize_in",),
    RESIZE_MODE_ITEMS[1][0]: ("fx_in", "fy_in"),
}


class OCVLresizeNode(OCVLNode):

    _doc = _("Resizes an image.")

    def update_layout(self, context):
        self.update_sockets(context)
        updateNode(self, context)

    image_in = StringProperty(name="image_in", default=str(uuid.uuid4()),
        description=_("Input image."))
    image_out = StringProperty(name="image_out", default=str(uuid.uuid4()),
        description=_("Output image."))

    dsize_in = IntVectorProperty(default=(100, 100), min=1, max=1024, size=2, update=updateNode,
        description=_("Output image size."))
    fx_in = FloatProperty(default=0.5, min=0.000001, max=0.999999, update=updateNode,
        description=_("Fx and fy and let the function compute the destination image size."))
    fy_in = FloatProperty(default=0.5, min=0.000001, max=0.999999, update=updateNode,
        description=_("Fx and fy and let the function compute the destination image size."))
    interpolation_in = EnumProperty(items=INTERPOLATION_ITEMS, default='INTER_NEAREST', update=updateNode,
        description=_("Interpolation method."))
    loc_resize_mode = EnumProperty(items=RESIZE_MODE_ITEMS, default="SIZE", update=update_layout,
        description=_("Loc resize mode."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "image_in")
        self.outputs.new("StringsSocket", "image_out")
        self.update_layout(context)

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])
        kwargs_inputs = self.get_kwargs_inputs(PROPS_MAPS, self.loc_resize_mode)

        kwargs = {
            'src': self.get_from_props("image_in"),
            'interpolation': self.get_from_props("interpolation_in"),
            }
        kwargs.update(kwargs_inputs)
        kwargs["dsize_in"] = kwargs.get("dsize_in", (0, 0))

        image_out = self.process_cv(fn=cv2.resize, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'loc_resize_mode', expand=True)
        self.add_button(layout, 'interpolation_in')

    def update_sockets(self, context):
        self.update_sockets_for_node_mode(PROPS_MAPS, self.loc_resize_mode)
        self.process()


def register():
    cv_register_class(OCVLresizeNode)


def unregister():
    cv_unregister_class(OCVLresizeNode)
