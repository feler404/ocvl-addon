import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLmultiplyNode(OCVLNodeBase):

    n_doc = "Calculates the per-element scaled product of two arrays."
    n_requirements = {"__and__": ["src1_in", "src2_in"]}

    src1_in: bpy.props.StringProperty(name="src1_in", default=str(uuid.uuid4()), description="First input array.")
    src2_in: bpy.props.StringProperty(name="src2_in", default=str(uuid.uuid4()), description="Second input array of the same size and type as src1.")
    scale_in: bpy.props.FloatProperty(name="scale_in", default=0.5, min=0, max=1, subtype="FACTOR" ,update=update_node, precision=4, description="Optional scale factor.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same size and type as src1.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src1_in")
        self.inputs.new("ImageSocket", "src2_in")
        self.inputs.new("StringsSocket", "scale_in").prop_name = "scale_in"
        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src1_in': self.get_from_props("src1_in"),
            'src2_in': self.get_from_props("src2_in"),
            'scale_in': self.get_from_props("scale_in"),
            }

        dst_out = self.process_cv(fn=cv2.multiply, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
