from bpy.props import StringProperty

from ...utils import cv_register_class, cv_unregister_class, OCVLPreviewNode
from ...auth import ocvl_auth


class OCVLImageViewerNode(OCVLPreviewNode):
    '''Image Viewer node'''
    bl_icon = 'ZOOM_ALL'

    image_in = StringProperty(default='')


    def sv_init(self, context):
        self.inputs.new('StringsSocket', "image_in")

    def wrapped_process(self):
        self.check_input_requirements(["image_in"])
        image = self.get_from_props("image_in")
        self.make_textures(image)

    def copy(self, node):
        self.n_id = ''
        self.process()
        node.process()

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.operator('image.image_full_screen', text='', icon="FULLSCREEN").origin = self.get_node_origin()
        self.draw_preview(layout=layout, prop_name="image_in", location_x=10, location_y=40)


if ocvl_auth.ocvl_ext:
    from ...extend.laboratory.ta_viewer_image import OCVLImageViewerNode


def register():
    cv_register_class(OCVLImageViewerNode)


def unregister():
    cv_unregister_class(OCVLImageViewerNode)
