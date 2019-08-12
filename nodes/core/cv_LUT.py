import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node
from ocvl.core.constants import NP_VALUE_TYPE_ITEMS


class OCVLLUTNode(OCVLNodeBase):

    n_doc = "Performs a look-up table transform of an array."
    n_requirements = {"__and__": ["src_in", "lut_in"]}
    n_quick_link_requirements = {
        "src_in": {"code_in": "COLOR_BGR2GRAY"}, "lut_in": {"size_in": 256, "loc_mode": "RANDOM"},
    }

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array of 8-bit elements.")
    lut_in: bpy.props.StringProperty(name="lut_in", default=str(uuid.uuid4()), description="Look-up table of 256 elements; in case of multi-channel input array, the table should either have a single channel (in this case the same table is used for all channels) or the same number of channels as in the input array.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output array of the same size and number of channels as src, and the same depth as lut.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new('OCVLVectorSocket', "lut_in")

        self.outputs.new("OCVLMatrixSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("src_in"),
            'lut_in': self.get_from_props("lut_in"),
        }

        dst_out = self.process_cv(fn=cv2.LUT, kwargs=kwargs)

        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
