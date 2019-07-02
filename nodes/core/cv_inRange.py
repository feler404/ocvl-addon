import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLinRangeNode(OCVLNodeBase):

    n_doc = "Checks if array elements lie between the elements of two other arrays."
    n_requirements = {"__and__": ["src_in", "lowerb_in", "upperb_in"]}
    n_quick_link_requirements = {
        "src_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
        "lowerb_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
        "upperb_in": {"code_in": "COLOR_BGR2GRAY", "value_type_in": "float32"},
    }

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="First input array.")
    lowerb_in: bpy.props.StringProperty(name="lowerb_in", default=str(uuid.uuid4()), description="Inclusive lower boundary array or a scalar.")
    upperb_in: bpy.props.StringProperty(name="upperb_in", default=str(uuid.uuid4()), description="Inclusive upper boundary array or a scalar.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same size as src and CV_8U type.")

    def init(self, context):
        self.inputs.new("ImageSocket", "src_in")
        self.inputs.new("ImageSocket", "lowerb_in")
        self.inputs.new("ImageSocket", "upperb_in")

        self.outputs.new("ImageSocket", "dst_out")

    def wrapped_process(self):

        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'lowerb_in': self.get_from_props("lowerb_in"),
            'upperb_in': self.get_from_props("upperb_in"),
            }

        dst_out = self.process_cv(fn=cv2.inRange, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
