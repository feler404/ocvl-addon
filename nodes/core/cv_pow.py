import uuid

import bpy
import cv2

from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLpowNode(OCVLNodeBase):

    n_doc = "Raises every array element to a power."
    n_requirements = {"__and__": ["src_in"]}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array.")
    power_in: bpy.props.IntProperty(name="power_in", default=2, min=0, max=100, update=update_node,description="Exponent of power.")

    dst_out: bpy.props.StringProperty(name="angle_out", default=str(uuid.uuid4()), description="Output array of the same size and type as src.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new("OCVLObjectSocket", "power_in").prop_name = "power_in"
        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'power_in': self.get_from_props("power_in"),
            }

        dst_out = self.process_cv(fn=cv2.pow, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
