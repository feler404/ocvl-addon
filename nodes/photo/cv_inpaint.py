import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


class OCVLinpaintNode(OCVLNodeBase):

    bl_flags_list = 'INPAINT_NS, INPAINT_TELEA'

    n_doc = "doc"
    n_quick_link_requirements = {"image_in": {"code_in": "COLOR_BGR2GRAY"}, "image_in": {"inpaintMask_in": "COLOR_BGR2GRAY", "color_in": (0, 0, 0, 0)}}
    n_requirements = {"__and__": ["image_in", "inpaintMask_in"]}

    image_in: bpy.props.StringProperty(name="image_in", default=str(uuid.uuid4()), description="desc")
    inpaintMask_in: bpy.props.StringProperty(name="inpaintMask_in", default=str(uuid.uuid4()), description="Inpainting mask, 8-bit 1-channel image. Non-zero pixels indicate the area that needs to be inpainted.")
    inpaintRadius_in: bpy.props.FloatProperty(default=3, min=1, max=10, update=update_node, description="Radius of a circular neighborhood of each point inpainted that is considered by the algorithm.")
    flags_in: bpy.props.BoolVectorProperty(default=[False for i in bl_flags_list.split(",")], size=len(bl_flags_list.split(",")), update=update_node, subtype="NONE", description=bl_flags_list)

    image_out: bpy.props.StringProperty(name="image_out", default=str(uuid.uuid4()), description="desc")

    def init(self, context):
        self.inputs.new("OCVLImageSocket", "image_in")
        self.inputs.new('OCVLMaskSocket', "inpaintMask_in")
        self.inputs.new('OCVLObjectSocket', "inpaintRadius_in").prop_name = 'inpaintRadius_in'

        self.outputs.new("OCVLImageSocket", "image_out")

    def wrapped_process(self):
        kwargs = {
            'src': self.get_from_props("image_in"),
            'inpaintMask_in': self.get_from_props("inpaintMask_in"),
            'inpaintRadius_in': self.get_from_props("inpaintRadius_in"),
            'flags_in': self.get_from_props("flags_in"),
            }

        image_out = self.process_cv(fn=cv2.inpaint, kwargs=kwargs)
        self.refresh_output_socket("image_out", image_out, is_uuid_type=True)

    def draw_buttons(self, context, layout):
        self.add_button(layout, "flags_in")
