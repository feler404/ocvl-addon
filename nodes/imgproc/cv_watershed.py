import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase


class OCVLwatershedNode(OCVLNodeBase):

    n_doc = "Performs a marker-based image segmentation using the watershed algorithm."
    n_development_status = "BETA"
    n_requirements = {"__and__": ["image_in"]}

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()), description="Input 8-bit 3-channel image.")
    markers_in: bpy.props.StringProperty(name="markers_in", default=str(uuid.uuid4()), description="Input/output 32-bit single-channel image (map) of markers. It should have the same size as image.")

    markers_out: bpy.props.StringProperty(name="markers_out", default=str(uuid.uuid4()), description="Markers output.")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "image_in")
        self.inputs.new("OCVLObjectSocket", "markers_in")

        self.outputs.new("OCVLObjectSocket", "markers_out")

    def wrapped_process(self):
        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'markers_in': self.get_from_props("markers_in"),
            }

        markers_out = self.process_cv(fn=cv2.watershed, kwargs=kwargs)
        self.refresh_output_socket("markers_out", markers_out, is_uuid_type=True)
