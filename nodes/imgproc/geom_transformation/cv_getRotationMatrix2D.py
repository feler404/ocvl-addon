import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLgetRotationMatrix2DNode(OCVLNodeBase):

    n_doc = "Calculates an affine matrix of 2D rotation."
    n_requirements = {}

    center_in: bpy.props.IntVectorProperty(default=(2, 2), min=1, max=30, size=2, update=update_node, description="Center of the rotation in the source image.")
    angle_in: bpy.props.FloatProperty(default=45, min=0, max=360, step=10, update=update_node, description="Rotation angle in degrees.")
    scale_in: bpy.props.FloatProperty(default=1, min=0, max=10, update=update_node, description="Isotropic scale factor.")

    retval_out: bpy.props.StringProperty(name="map_matrix", default=str(uuid.uuid4()), description="The output affine transformation, 2x3 floating-point matrix.")

    def init(self, context):
        self.width = 180
        self.inputs.new("OCVLObjectSocket", "center_in").prop_name = "center_in"
        self.inputs.new("OCVLObjectSocket", "angle_in").prop_name = "angle_in"
        self.inputs.new("OCVLObjectSocket", "scale_in").prop_name = "scale_in"

        self.outputs.new("OCVLObjectSocket", "retval_out")

    def wrapped_process(self):
        kwargs = {
            'center_in': self.get_from_props("center_in"),
            'angle_in': self.get_from_props("angle_in"),
            'scale_in': self.get_from_props("scale_in"),
            }

        retval_out = self.process_cv(fn=cv2.getRotationMatrix2D, kwargs=kwargs)
        self.refresh_output_socket("retval_out", retval_out, is_uuid_type=True)
