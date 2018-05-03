import cv2
import uuid
from gettext import gettext as _
from bpy.props import EnumProperty, StringProperty, BoolProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLNode, updateNode


OUTPUT_MAP_TYPE_ITEMS = (
    ("CV_16SC2", "CV_16SC2", "CV_16SC2", "", 0),
    ("CV_32FC1", "CV_32FC1", "CV_32FC1", "", 1),
    ("CV_32FC2", "CV_32FC2", "CV_32FC2", "", 2),
)


class OCVLconvertMapsNode(OCVLNode):

    _doc = _("Converts image transformation maps from one representation to another.")

    map1_in = StringProperty(name="map1_in", default=str(uuid.uuid4()),
        description=_("The first input map of type CV_16SC2 , CV_32FC1 , or CV_32FC2 ."))
    map2_in = StringProperty(name="map2_in", default=str(uuid.uuid4()),
        description=_("The second input map of type CV_16UC1 , CV_32FC1 , or none (empty matrix), respectively."))
    dstmap1_out = StringProperty(name="dstmap1_out", default=str(uuid.uuid4()),
        description=_("The first output map that has the type dstmap1type and the same size as src ."))
    dstmap2_out = StringProperty(name="dstmap2_out", default=str(uuid.uuid4()),
        description=_("The second output map."))

    dstmap1type_in = EnumProperty(items=OUTPUT_MAP_TYPE_ITEMS, default='CV_16SC2', update=updateNode,
        description=_("Type of the first output map that should be."))
    nninterpolation_in = BoolProperty(default=False, update=updateNode,
        description=_("Flag indicating whether the fixed-point maps are used for the nearest-neighbor or for a more complex interpolation."))

    def sv_init(self, context):
        self.inputs.new("StringsSocket", "map1_in")
        self.inputs.new('StringsSocket', "map2_in")

        self.outputs.new("StringsSocket", "dstmap1_out")
        self.outputs.new("StringsSocket", "dstmap2_out")

    def wrapped_process(self):
        self.check_input_requirements(["map1_in", "map2_in"])

        kwargs = {
            'map1_in': self.get_from_props("map1_in"),
            'map2_in': self.get_from_props("map2_in"),
            'dstmap1type_in': self.get_from_props("dstmap1type_in"),
            'nninterpolation_in': self.get_from_props("nninterpolation_in"),
            }

        dstmap1_out, dstmap2_out = self.process_cv(fn=cv2.convertMaps, kwargs=kwargs)
        self.refresh_output_socket("dstmap1_out", dstmap1_out, is_uuid_type=True)
        self.refresh_output_socket("dstmap2_out", dstmap2_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'dstmap1type_in')
        self.add_button(layout, 'nninterpolation_in')


def register():
    cv_register_class(OCVLconvertMapsNode)


def unregister():
    cv_unregister_class(OCVLconvertMapsNode)
