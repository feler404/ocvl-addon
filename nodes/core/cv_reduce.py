import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node, REDUCE_TYPES_ITEMS


class OCVLreduceNode(OCVLNodeBase):

    n_doc = "Reduces a matrix to a vector."
    n_requirements = {"__and__": ["src_in"]}
    n_quick_link_requirements = {"dst_in": {"code_in": "COLOR_BGR2GRAY"}}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()),  description="Input 2D matrix.")
    dim_in: bpy.props.IntProperty(name="dim_in", default=0, min=0, max=1, update=update_node, description="dimension index along which the matrix is reduced.")
    rtype_in: bpy.props.EnumProperty(items=REDUCE_TYPES_ITEMS, default='REDUCE_AVG', update=update_node, description="Reduction operation that could be one of the following, see cv::ReduceTypes.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output vector. Its size and type is defined by dim and dtype parameters.")

    def init(self, context):
        self.width = 150
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new("StringsSocket", "dim_in").prop_name = "dim_in"

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'rtype_in': self.get_from_props("rtype_in"),
            'dim_in': self.get_from_props("dim_in"),
            }

        dst_out = self.process_cv(fn=cv2.reduce, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "rtype_in")