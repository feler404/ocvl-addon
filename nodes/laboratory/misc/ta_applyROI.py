import uuid

import bpy
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLApplyROINode(OCVLNodeBase):

    n_doc = "Insert ROI to other image."
    n_requirements = {"__and__": ["image_in", "image_roi_in"]}
    n_quick_link_requirements = {
        "image_in": {"width_in": 100, "height_in": 100, "loc_image_mode": "PLANE"},
        "image_roi_in": {"width_in": 30, "height_in": 30},
    }

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()))
    image_roi_in: bpy.props.StringProperty(name="image_roi_in", default=str(uuid.uuid4()))
    pt1_in: bpy.props.IntVectorProperty(default=(30, 30), size=2, min=0, update=update_node, description="Upper left corner ROI inserting.")

    image_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()))

    def init(self, context):
        self.width = 200
        self.inputs.new("OCVLImageSocket", "image_in")
        self.inputs.new("OCVLImageSocket", "image_roi_in")
        self.inputs.new('OCVLMatrixSocket', "pt1_in").prop_name = 'pt1_in'

        self.outputs.new("OCVLImageSocket", "image_out")

    def wrapped_process(self):
        image_in = self.get_from_props("image_in")
        image_roi_in = self.get_from_props("image_roi_in")
        pt1_in = self.get_from_props("pt1_in")

        image_out = image_in.copy()
        image_out[pt1_in[0]:image_roi_in.shape[0] + pt1_in[0], pt1_in[1]:image_roi_in.shape[1] + pt1_in[1]] = image_roi_in
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)
