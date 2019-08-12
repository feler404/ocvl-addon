import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLgetRectSubPixNode(OCVLNodeBase):

    n_doc = "Retrieves a pixel rectangle from an image with sub-pixel accuracy."
    n_requirements = {"__and__": ["image_in"]}

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()), description="Source image.")
    patchSize_in: bpy.props.IntVectorProperty(default=(5, 5), min=1, max=30, size=2, update=update_node, description="Size of the extracted patch.")
    center_in: bpy.props.IntVectorProperty(default=(2, 2), min=1, max=30, size=2, update=update_node, description="Floating point coordinates of the center of the extracted rectangle.")
    patchType_in: bpy.props.IntProperty(default=-1, min=-1, max=30, update=update_node, description="Depth of the extracted pixels. By default, they have the same depth as src.")

    patch_out: bpy.props.StringProperty(name="patch_out", default=str(uuid.uuid4()), description="Patch out")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "image_in")
        self.inputs.new("OCVLObjectSocket", "patchSize_in").prop_name = "patchSize_in"
        self.inputs.new("OCVLObjectSocket", "center_in").prop_name = "center_in"
        self.inputs.new("OCVLObjectSocket", "patchType_in").prop_name = "patchType_in"

        self.outputs.new("OCVLObjectSocket", "patch_out")

    def wrapped_process(self):
        kwargs = {
            'image_in': self.get_from_props("image_in"),
            'patchSize_in': self.get_from_props("patchSize_in"),
            'center_in': self.get_from_props("center_in"),
            'patchType_in': self.get_from_props("patchType_in"),
            }

        patch_out = self.process_cv(fn=cv2.getRectSubPix, kwargs=kwargs)
        self.refresh_output_socket("patch_out", patch_out, is_uuid_type=True)
