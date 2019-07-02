import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


FLIP_CODE_ITEMS = (
    ("0", "Vertical", "Vertical", "", 0),
    ("1", "Horizontal", "Horizontal", "", 1),
    ("-1", "Simultaneous", "Simultaneous    ", "", 2),
)


class OCVLflipNode(OCVLNodeBase):

    n_doc = "Flips a 2D array around vertical, horizontal, or both axes."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array.")
    flipCode_in: bpy.props.EnumProperty(items=FLIP_CODE_ITEMS, default='0', update=update_node, description="Flag to specify how to flip the array.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same size and type as src.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):

        kwargs = {
            'src': self.get_from_props("src_in"),
            'flipCode_in': int(self.get_from_props("flipCode_in")),
            }

        dst_out = self.process_cv(fn=cv2.flip, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'flipCode_in', expand=True)
