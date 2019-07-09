import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, BORDER_TYPE_ITEMS


class OCVLblurNode(OCVLNodeBase):

    bl_icon = 'FILTER'

    n_doc = "Blurs an image using the normalized box filter."
    n_requirements = {"__and__": ["src_in"]}

    def get_anchor(self):
        return self.get("anchor_in", (-1, -1))

    def set_anchor(self, value):
        anchor_x = value[0] if -1 <= value[0] < self.ksize_in[0] else self.anchor_in[0]
        anchor_y = value[1] if -1 <= value[1] < self.ksize_in[1] else self.anchor_in[1]
        self["anchor_in"] = (anchor_x, anchor_y)

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input image.")
    ksize_in: bpy.props.IntVectorProperty(default=(1, 10), update=update_node, min=1, max=30, size=2, description="Blurring kernel size.")
    anchor_in: bpy.props.IntVectorProperty(default=(-1, -1), min=-1, max=30, update=update_node, get=get_anchor, set=set_anchor, size=2, description="Bnchor point; default value Point(-1,-1) means that the anchor is at the kernel center.")
    borderType_in: bpy.props.EnumProperty(items=BORDER_TYPE_ITEMS, default='None', update=update_node, description="Border mode used to extrapolate pixels outside of the image, see cv::BorderTypes.")

    dst_in: bpy.props.StringProperty(name="dst_in", default=str(uuid.uuid4()), description="Output image.")

    def init(self, context):
        self.width = 250
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new('StringsSocket', "ksize_in").prop_name = 'ksize_in'
        self.inputs.new('StringsSocket', "anchor_in").prop_name = 'anchor_in'

        self.outputs.new("ImageSocket", "dst_in")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("src_in"),
            'ksize_in': self.get_from_props("ksize_in"),
            'anchor_in': self.get_from_props("anchor_in"),
            'borderType_in': self.get_from_props("borderType_in"),
            }

        dst_in = self.process_cv(fn=cv2.blur, kwargs=kwargs)
        self.refresh_output_socket("dst_in", dst_in, is_uuid_type=True)

    def generate_code(self, prop_name, exit_prop_name):
        lines = []
        if prop_name == 'dst_in':
            if self.inputs["src_in"].is_linked:
                node_linked = self.inputs["src_in"].links[0].from_node
                socket_name = self.inputs["src_in"].links[0].from_socket.name
                lines.extend(node_linked.generate_code(socket_name, "src"))
            lines.append('ksize_in = {}'.format(self.get_from_props("ksize_in")))
            lines.append("{} = cv2.blur(src=src, ksize_in=ksize_in)".format(exit_prop_name))
        return lines

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'borderType_in')
