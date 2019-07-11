import bpy
import numpy as np

from ocvl.core.node_base import OCVLPreviewNodeBase


VALID_INPUT_DTYPES = (np.dtype('uint8'), np.dtype('uint16'), np.dtype('float32'))


class OCVLImageViewerNode(OCVLPreviewNodeBase):
    """
    Image Viewer node
    """
    bl_icon = 'ZOOM_ALL'

    n_doc = "Image viewer"

    image_in: bpy.props.StringProperty(default='')

    def init(self, context):
        self.inputs.new('ImageSocket', "image_in")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])
        image = self.get_from_props("image_in")
        if image.dtype not in VALID_INPUT_DTYPES:
            image = image.astype("uint8")
        self.make_textures(image)

    def generate_code(self):
        lines = []
        img_name = "img_{}".format(self.name)

        if self.inputs["image_in"].is_linked:
            node_linked = self.inputs["image_in"].links[0].from_node
            socket_name = self.inputs["image_in"].links[0].from_socket.name
            lines.extend(node_linked.generate_code(socket_name, img_name))
        lines.append("cv2.imshow({})".format(img_name))
        print("\n".join(lines))

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.operator('image.image_full_screen', text='', icon="PLUS").origin = self.get_node_origin()
        # col.operator('node.generate_python_code', text='', icon="FULLSCREEN").origin = self.get_node_origin()
        self.draw_preview(layout=layout, prop_name="image_in", location_x=10, location_y=-60)
