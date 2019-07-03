import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLmulTransposedNode(OCVLNodeBase):

    n_doc = "Calculates the product of a matrix and its transposition."
    n_requirements = {"__and__": ["src_in"]}
    n_quick_link_requirements = {"src_in": {"code_in": "COLOR_BGR2GRAY"}, "delta_in": {"code_in": "COLOR_BGR2GRAY"}}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="First input array.")
    aTa_in: bpy.props.BoolProperty(name="aTa_in", default=True, update=update_node, description="Flag specifying the multiplication ordering.")
    delta_in: bpy.props.StringProperty(name="delta_in", default=str(uuid.uuid4()), description="Optional delta matrix subtracted from src before the multiplication.")
    scale_in: bpy.props.FloatProperty(name="scale_in", default=0.5, min=0, max=1, subtype="FACTOR", update=update_node, precision=4, description="Optional scale factor.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same size and type as src1.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new("ImageSocket", "delta_in")
        self.inputs.new("StringsSocket", "scale_in").prop_name = "scale_in"
        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'aTa_in': self.get_from_props("aTa_in"),
            'delta_in': self.get_from_props("delta_in"),
            'scale_in': self.get_from_props("scale_in"),
            }

        if isinstance(kwargs["delta_in"], str):
            kwargs.pop("delta_in")

        dst_out = self.process_cv(fn=cv2.mulTransposed, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
