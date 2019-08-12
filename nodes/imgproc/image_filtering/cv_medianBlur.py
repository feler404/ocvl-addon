import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node, BORDER_TYPE_ITEMS


class OCVLmedianBlurNode(OCVLNodeBase):
    n_doc = "The function smoothes an image using the median filter with the ksize aperture. Each channel of a multi-channel image is processed independently. In-place operation is supported."
    n_see_also = "bileteralFilter,blur,boxFilter,GaussianBlur"
    n_requirements = {"__and__": ["src_in"]}

    def set_ksize(self, value):
        if value % 2 == 0:
            value = value + 1
        self["ksize_in"] = value

    def get_ksize(self):
        return self.get("ksize_in", 5)

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input 1-, 3-, or 4-channel image; when ksize is 3 or 5, the image depth should be CV_8U, CV_16U, or CV_32F, for larger aperture sizes, it can only be CV_8U.")
    ksize_in: bpy.props.IntProperty(default=5, update=update_node, min=1, max=30, get=get_ksize, set=set_ksize, description="Aperture linear size; it must be odd and greater than 1, for example: 3, 5, 7 ...")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Destination array of the same size and type as src.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "src_in")
        self.inputs.new('OCVLMatrixSocket', "ksize_in").prop_name = 'ksize_in'

        self.outputs.new("OCVLImageSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
            'ksize_in': self.get_from_props("ksize_in"),
        }

        dst_out = self.process_cv(fn=cv2.medianBlur, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
