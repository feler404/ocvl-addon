import uuid
import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLconvertPointsHomogeneousNode(OCVLNodeBase):

    n_doc = "Converts points to/from homogeneous coordinates."
    n_requirements = {"__and__": ["src_in"]}
    n_quick_link_requirements = {"src_in": {"loc_input_mode": "MANUAL", "value_type_in": "float32", "loc_manual_input": "[[0, 0], [1,1], [2, 2]]"}}

    src_in: bpy.props.StringProperty(name="src_in", default=str(uuid.uuid4()), description="Input array or vector of 2D, 3D, or 4D points.")

    dst_out: bpy.props.StringProperty(name="dst_out", default=str(uuid.uuid4()), description="Output vector of 2D, 3D, or 4D points.")

    def init(self, context):
        self.inputs.new("OCVLVectorSocket", "src_in")

        self.outputs.new("OCVLObjectSocket", "dst_out")

    def wrapped_process(self):
        kwargs = {
            'src_in': self.get_from_props("src_in"),
        }

        dst_out= self.process_cv(fn=cv2.convertPointsToHomogeneous, kwargs=kwargs)
        self.refresh_output_socket("dst_out", dst_out, is_uuid_type=True)
