import uuid
import time
import cv2
import bpy
import bgl
import numpy as np
from itertools import chain
from uuid import UUID
from logging import getLogger
from bpy.props import StringProperty

from . import IS_WORK_ON_COPY_INPUT, OCVL_EXT
from .sverchok_point import SverchCustomTreeNode, node_id, nodeview_bgl_viewer_draw_mk2, sv_preferences
from sverchok.core.socket_data import SvNoDataError

logger = getLogger(__name__)
nvBGL2 = nodeview_bgl_viewer_draw_mk2
sv_preferences = sv_preferences

NODE_COLOR_REQUIRE_DATE = (1, 0.3, 0)


if not hasattr(np, 'opencv_handler'):
    np.opencv_handler = {}
    np.opencv_handler['GARBAGE_TEXTURES'] = []


GL_COLOR_DICT = {
    'BW': 6409,  # GL_LUMINANCE
    'RGB': 6407,  # GL_RGB
    'RGBA': 6408  # GL_RGBA
}


FACTOR_BUFFER_DICT = {
    'BW': 1,  # GL_LUMINANCE
    'RGB': 3,  # GL_RGB
    'RGBA': 4  # GL_RGBA
}

TEX_CO = [(0, 1), (1, 1), (1, 0), (0, 0)]
TEX_CO_FLIP = [(0, 0), (1, 0), (1, 1), (0, 1)]

APPROXIMATION_MODE_ITEMS = (
    # https://docs.opencv.org/3.3.1/d3/dc0/group__imgproc__shape.html#ga4303f45752694956374734a03c54d5ff
    ("CHAIN_APPROX_SIMPLE", "CHAIN_APPROX_SIMPLE", "CHAIN_APPROX_SIMPLE", "", 0),
    ("CHAIN_APPROX_NONE", "CHAIN_APPROX_NONE", "CHAIN_APPROX_NONE", "", 1),
    ("CHAIN_APPROX_TC89_L1", "CHAIN_APPROX_TC89_L1", "CHAIN_APPROX_TC89_L1", "", 2),
    ("CHAIN_APPROX_TC89_KCOS", "CHAIN_APPROX_TC89_KCOS", "CHAIN_APPROX_TC89_KCOS", "", 3),
    )
BORDER_TYPE_ITEMS = (
    ("BORDER_CONSTANT", "BORDER_CONSTANT", "BORDER_CONSTANT", "", 0),
    ("BORDER_DEFAULT", "BORDER_DEFAULT", "BORDER_DEFAULT", "", 1),
    ("BORDER_ISOLATED", "BORDER_ISOLATED", "BORDER_ISOLATED", "", 2),
    ("BORDER_REFLECT", "BORDER_REFLECT", "BORDER_REFLECT", "", 3),
    ("BORDER_REFLECT101", "BORDER_REFLECT101", "BORDER_REFLECT101", "", 4),
    ("BORDER_REPLICATE", "BORDER_REPLICATE", "BORDER_REPLICATE", "", 5),
    ("BORDER_TRANSPARENT", "BORDER_TRANSPARENT", "BORDER_TRANSPARENT", "", 6),
    ("BORDER_WRAP", "BORDER_WRAP", "BORDER_WRAP", "", 7),
    ("None", "None", "None", "", 8),
    )
BORDER_MODE_ITEMS = (
    ("BORDER_CONSTANT", "BORDER_CONSTANT", "BORDER_CONSTANT", "", 0),
    ("BORDER_REPLICATE", "BORDER_REPLICATE", "BORDER_REPLICATE", "", 1),
)
BORDER_TYPE_REQUIRED_ITEMS = BORDER_TYPE_ITEMS[:9]
CODE_COLOR_POOR_ITEMS = (
    ("COLOR_BGR2GRAY", "COLOR_BGR2GRAY", "COLOR_BGR2GRAY", "", 0),
    ("COLOR_BGR2RGB", "COLOR_BGR2RGB", "COLOR_BGR2RGB", "", 1),
    ("COLOR_BGR2HLS", "COLOR_BGR2HLS", "COLOR_BGR2HLS", "", 2),
    ("COLOR_BGR2HSV", "COLOR_BGR2HSV", "COLOR_BGR2HSV", "", 3),
    ("COLOR_BGR2LAB", "COLOR_BGR2LAB", "COLOR_BGR2LAB", "", 4),
    ("COLOR_BGR2LUV", "COLOR_BGR2LUV", "COLOR_BGR2LUV", "", 5),
    ("COLOR_BGR2YCR_CB", "COLOR_BGR2YCR_CB", "COLOR_BGR2YCR_CB", "", 6),
    ("COLOR_BGR2YUV", "COLOR_BGR2YUV", "COLOR_BGR2YUV", "", 7),
)
COLOR_DEPTH_ITEMS = [
    ("CV_8U", "CV_8U", "CV_8U", "", 1),
    ("CV_16U", "CV_16U", "CV_16U", "", 2),
    ]
COLOR_DEPTH_WITH_NONE_ITEMS = (
    ("None", "None", "None", "", 0),
    ("CV_8U", "CV_8U", "CV_8U", "", 1),
    ("CV_16U", "CV_16U", "CV_16U", "", 2),
)
COEFFICIENTS_TYPE_ITEMS = (
    ("CV_32F", "CV_32F", "CV_32F", "", 0),
    ("CV_64F", "CV_64F", "CV_64F", "", 1),
)
DISTANCE_TYPE_ITEMS = (
    ("DIST_C", "DIST_C", "DIST_C", "", 1),
    ("DIST_L1", "DIST_L1", "DIST_L1", "", 2),
    ("DIST_LABEL_CCOMP", "DIST_LABEL_CCOMP", "DIST_LABEL_CCOMP", "", 3),
    ("DIST_MASK_5", "DIST_MASK_5", "DIST_MASK_5", "", 4),
    ("DIST_WELSCH", "DIST_WELSCH", "DIST_WELSCH", "", 5),
    ("DIST_FAIR", "DIST_FAIR", "DIST_FAIR", "", 6),
    ("DIST_L12", "DIST_L12", "DIST_L12", "", 7),
    ("DIST_LABEL_PIXEL", "DIST_LABEL_PIXEL", "DIST_LABEL_PIXEL", "", 8),
    ("DIST_MASK_PRECISE", "DIST_MASK_PRECISE", "DIST_MASK_PRECISE", "", 9),
    ("DIST_HUBER", "DIST_HUBER", "DIST_HUBER", "", 10),
    ("DIST_L2", "DIST_L2", "DIST_L2", "", 11),
    ("DIST_MASK_3", "DIST_MASK_3", "DIST_MASK_3", "", 12),
    ("DIST_USER", "DIST_USER", "DIST_USER", "", 13),
)
DISTANCE_TYPE_FOR_TRANSFORM_ITEMS = (
    ("DIST_C", "DIST_C", "DIST_C", "", 0),
    ("DIST_L1", "DIST_L1", "DIST_L1", "", 1),
    ("DIST_L2", "DIST_L2", "DIST_L2", "", 2),
)
FONT_FACE_ITEMS = [
        ('FONT_HERSHEY_COMPLEX', 'FONT_HERSHEY_COMPLEX', 'FONT_HERSHEY_COMPLEX', "", 1),
        ('FONT_HERSHEY_COMPLEX_SMALL', 'FONT_HERSHEY_COMPLEX_SMALL', 'FONT_HERSHEY_COMPLEX_SMALL', "", 2),
        ('FONT_HERSHEY_DUPLEX', 'FONT_HERSHEY_DUPLEX', 'FONT_HERSHEY_DUPLEX', "", 3),
        ('FONT_HERSHEY_PLAIN', 'FONT_HERSHEY_PLAIN', 'FONT_HERSHEY_PLAIN', "", 4),
        ('FONT_HERSHEY_SCRIPT_COMPLEX', 'FONT_HERSHEY_SCRIPT_COMPLEX', 'FONT_HERSHEY_SCRIPT_COMPLEX', "", 5),
        ('FONT_HERSHEY_SCRIPT_SIMPLEX', 'FONT_HERSHEY_SCRIPT_SIMPLEX', 'FONT_HERSHEY_SCRIPT_SIMPLEX', "", 6),
        ('FONT_HERSHEY_SIMPLEX', 'FONT_HERSHEY_SIMPLEX', 'FONT_HERSHEY_SIMPLEX', "", 7),
        ('FONT_HERSHEY_TRIPLEX', 'FONT_HERSHEY_TRIPLEX', 'FONT_HERSHEY_TRIPLEX', "", 8),
        ('FONT_ITALIC', 'FONT_ITALIC', 'FONT_ITALIC', "", 9),
    ]
INTERPOLATION_ITEMS = [
    ('INTER_AREA', 'INTER_AREA', 'INTER_AREA', '', 0),
    ('INTER_BITS', 'INTER_BITS', 'INTER_BITS', '', 1),
    ('INTER_BITS2', 'INTER_BITS2', 'INTER_BITS2', '', 2),
    ('INTER_CUBIC', 'INTER_CUBIC', 'INTER_CUBIC', '', 3),
    ('INTER_LANCZOS4', 'INTER_LANCZOS4', 'INTER_LANCZOS4', '', 4),
    ('INTER_LINEAR', 'INTER_LINEAR', 'INTER_LINEAR', '', 5),
    ('INTER_MAX', 'INTER_MAX', 'INTER_MAX', '', 6),
    ('INTER_NEAREST', 'INTER_NEAREST', 'INTER_NEAREST', '', 7),
    ('INTER_TAB_SIZE', 'INTER_TAB_SIZE', 'INTER_TAB_SIZE', '', 8),
    ('INTER_TAB_SIZE2', 'INTER_TAB_SIZE2', 'INTER_TAB_SIZE2', '', 9),
]
LINE_TYPE_ITEMS = (
    ("LINE_AA", "LINE_AA", "LINE_AA", "", 0),
    ("LINE_8", "LINE_8", "LINE_8", "", 1),
    ("LINE_4", "LINE_4", "LINE_4", "", 2),
)
NORMALIZATION_TYPE_ITEMS = (
    ("NORMAL_CLONE", "NORMAL_CLONE", "NORMAL_CLONE", "", 0),
    ("NORMCONV_FILTER", "NORMCONV_FILTER", "NORMCONV_FILTER", "", 1),
    ("NORM_HAMMING", "NORM_HAMMING", "NORM_HAMMING", "", 2),
    ("NORM_HAMMING2", "NORM_HAMMING2", "NORM_HAMMING2", "", 3),
    ("NORM_INF", "NORM_INF", "NORM_INF", "", 4),
    ("NORM_L1", "NORM_L1", "NORM_L1", "", 5),
    ("NORM_L2", "NORM_L2", "NORM_L2", "", 6),
    ("NORM_L2SQR", "NORM_L2SQR", "NORM_L2SQR", "", 7),
    ("NORM_MINMAX", "NORM_MINMAX", "NORM_MINMAX", "", 8),
    ("NORM_RELATIVE", "NORM_RELATIVE", "NORM_RELATIVE", "", 9),
    ("NORM_TYPE_MASK", "NORM_TYPE_MASK", "NORM_TYPE_MASK", "", 10),
)
MORPH_TYPE_ITEMS = (
    ("MORPH_BLACKHAT", "MORPH_BLACKHAT", "MORPH_BLACKHAT", "", 0),
    ("MORPH_CLOSE", "MORPH_CLOSE", "MORPH_CLOSE", "", 1),
    ("MORPH_CROSS", "MORPH_CROSS", "MORPH_CROSS", "", 2),
    ("MORPH_DILATE", "MORPH_DILATE", "MORPH_DILATE", "", 3),
    ("MORPH_ELLIPSE", "MORPH_ELLIPSE", "MORPH_ELLIPSE", "", 4),
    ("MORPH_ERODE", "MORPH_ERODE", "MORPH_ERODE", "", 5),
    ("MORPH_GRADIENT", "MORPH_GRADIENT", "MORPH_GRADIENT", "", 6),
    ("MORPH_HITMISS", "MORPH_HITMISS", "MORPH_HITMISS", "", 7),
    ("MORPH_OPEN", "MORPH_OPEN", "MORPH_OPEN", "", 8),
    ("MORPH_RECT", "MORPH_RECT", "MORPH_RECT", "", 9),
    ("MORPH_TOPHAT", "MORPH_TOPHAT", "MORPH_TOPHAT", "", 10),
)
RETRIEVAL_MODE_ITEMS = [
    # https://docs.opencv.org/3.3.1/d3/dc0/group__imgproc__shape.html#ga819779b9857cc2f8601e6526a3a5bc71
    ("RETR_TREE", "RETR_TREE", "RETR_TREE", "", 0),
    ("RETR_LIST", "RETR_LIST", "RETR_LIST", "", 1),
    ("RETR_CCOMP", "RETR_CCOMP", "RETR_CCOMP", "", 2),
    ("RETR_EXTERNAL", "RETR_EXTERNAL", "RETR_EXTERNAL", "", 3),
    ("RETR_FLOODFILL", "RETR_FLOODFILL", "RETR_FLOODFILL", "", 4),
    ]
TEMPLATE_MATCH_MODE_ITEMS = (
    ("TM_CCOEFF", "TM_CCOEFF", "TM_CCOEFF", "", 0),
    ("TM_CCOEFF_NORMED", "TM_CCOEFF_NORMED", "TM_CCOEFF_NORMED", "", 1),
    ("TM_CCORR", "TM_CCORR", "TM_CCORR", "", 2),
    ("TM_CCORR_NORMED", "TM_CCORR_NORMED", "TM_CCORR_NORMED", "", 3),
    ("TM_SQDIFF", "TM_SQDIFF", "TM_SQDIFF", "", 4),
    ("TM_SQDIFF_NORMED", "TM_SQDIFF_NORMED", "TM_SQDIFF_NORMED", "", 5),
)
TYPE_THRESHOLD_ITEMS = (
    ("THRESH_BINARY", "THRESH_BINARY", "THRESH_BINARY", "", 0),
    ("THRESH_BINARY_INV", "THRESH_BINARY_INV", "THRESH_BINARY_INV", "", 1),
    ("THRESH_TRUNC", "THRESH_TRUNC", "THRESH_TRUNC", "", 2),
    ("THRESH_TOZERO", "THRESH_TOZERO", "THRESH_TOZERO", "", 3),
    ("THRESH_TOZERO_INV", "THRESH_TOZERO_INV", "THRESH_TOZERO_INV", "", 4),
    ("THRESH_MASK", "THRESH_MASK", "THRESH_MASK", "", 5),
    ("THRESH_OTSU", "THRESH_OTSU", "THRESH_OTSU", "", 6),
    ("THRESH_TRIANGLE", "THRESH_TRIANGLE", "THRESH_TRIANGLE", "", 7),
    )


DEVELOP_STATE_ALPHA = "ALPHA"
DEVELOP_STATE_BETA = "BETA"
DEVELOP_STATE_RC = "RC"
DEVELOP_STATE_PROD = "PROD"


IS_WORK_ON_COPY_INPUT = IS_WORK_ON_COPY_INPUT
SCALE = bpy.context.user_preferences.system.pixel_size
LAST_PIC = time.time()
socket_data_cache = np.opencv_handler
np.bl_listener = None
np.LAST_PIC = time.time()


class OCVLNodeException(Exception):
    pass


class LackRequiredSocket(OCVLNodeException):
    pass


class MockSocket:
    data = {}

    def __init__(self, data):
        self.data['data'] = data
        self.data['type'] = type(data)
        self.data['shape'] = getattr(data, "shape", None)
        self.data['size'] = getattr(data, "size", None)

    def sv_get(self, *args, **kwargs):
        return self.data


def updateNode(self, context):
    self.process_node(context)


def convert_to_gl_image(image_cv):
    image_cv = cv2.flip(image_cv, 0)
    if len(image_cv.shape) == 3:
        image_gl = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGBA) / 255
    if len(image_cv.shape) == 2:
        r = g = b = image_cv / 255
        a = np.ones(image_cv.shape, dtype=r.dtype)
        image_gl = cv2.merge((r, g, b, a))
    image_gl.astype(np.uint8)
    return image_gl


def convert_to_cv_image(image_gl):
    image_cv = np.array(image_gl.pixels, dtype=np.float32)
    image_cv = image_cv.reshape((image_gl.size[1], image_gl.size[0], image_gl.channels))
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGBA2BGR) * 255
    image_cv = cv2.flip(image_cv, 0)
    image_cv.astype(np.uint8)
    return image_cv


def init_texture(width, height, texname, texture, internalFormat, format):
    bgl.glEnable(bgl.GL_TEXTURE_2D)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, texname)
    bgl.glActiveTexture(bgl.GL_TEXTURE0)
    bgl.glTexParameterf(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_S, bgl.GL_CLAMP)
    bgl.glTexParameterf(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_T, bgl.GL_CLAMP)
    bgl.glTexParameterf(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_LINEAR)
    bgl.glTexParameterf(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_LINEAR)
    bgl.glTexImage2D(
        bgl.GL_TEXTURE_2D,
        0, internalFormat, width, height,
        0, format, bgl.GL_UNSIGNED_BYTE, texture
    )


def simple_screen(x, y, args):
    texture, texname, width, height, r, g, b, alpha, tex_co = args

    def draw_texture(x=0, y=0, w=30, h=10, texname=texname, r=1.0, g=1.0, b=1.0, alpha=0.9, tex_co=TEX_CO):
        bgl.glDisable(bgl.GL_DEPTH_TEST)
        bgl.glActiveTexture(bgl.GL_TEXTURE0)
        bgl.glEnable(bgl.GL_TEXTURE_2D)

        bgl.glColor4f(r, g, b, alpha)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, texname)

        SCALE = bpy.context.user_preferences.system.pixel_size
        x *= SCALE; y *= SCALE
        verco = [(x, y), (x + w, y), (x + w, y - h), (x, y - h)]
        bgl.glBegin(bgl.GL_QUADS)

        for i in range(4):
            bgl.glTexCoord3f(tex_co[i][0], tex_co[i][1], 0.0)
            bgl.glVertex2f(verco[i][0], verco[i][1])

        bgl.glEnd()

        bgl.glDisable(bgl.GL_TEXTURE_2D)

    draw_texture(x=x, y=y, w=width, h=height, texname=texname, r=r, g=g, b=b, alpha=alpha, tex_co=tex_co)


def on_click_callback(x, y, button, pressed):
    if 'bpy' not in globals():
        return True
    if bpy.data.window_managers['WinMan'].operators[-1].name == 'Hide':
        for node_group in bpy.data.node_groups:
            if node_group.nodes.active:
                node_group.nodes.active._draw_preview(hide=True)
                return True
    return True


class OCVLNode(bpy.types.Node, SverchCustomTreeNode):
    socket_data_cache = socket_data_cache
    n_meta = ""

    def is_uuid(self, prop):
        try:
            UUID(prop)
            return True
        except (ValueError, AttributeError):
            return False

    def _get_flag_from_prop(self):
        selected_flags = self.flags_in
        ret = 0
        for i, flag_name in enumerate(self.bl_flags_list.split(",")):
            if selected_flags[i]:
                ret += getattr(cv2, flag_name.strip(), 0)
        return ret

    def _get_image_in_from_prop(self):
        socket = self.inputs.get("image_in")
        try:
            prop = socket.sv_get()
            return self.socket_data_cache[prop]
        except SvNoDataError as e:
            fn = getattr(self, "report", print)
            fn({'INFO'}, "No data in props: {}".format("image_in"))
            raise
        return np.zeros([10, 10], np.uint8)

    def _is_linked(self, key):
        return self.inputs.get(key) and self.inputs.get(key).is_linked

    def get_from_props(self, key, is_color=False):
        if key == "image_out":
            return self.socket_data_cache[self.image_out]
        elif key == "flags_in":
            return self._get_flag_from_prop()
        elif key == "image_in":
            return self._get_image_in_from_prop()
        elif key == "dtype_in":
            return getattr(cv2, self.dtype_in, -1)

        if self._is_linked(key):
            socket = self.inputs.get(key)
            prop = socket.sv_get()
            if isinstance(prop, (int, float, bool)):
                return prop
            elif isinstance(prop, (str,)):
                if self.is_uuid(prop):
                    return self.socket_data_cache[prop]
                else:
                    return prop
            elif len(prop[0]) > 1:
                return tuple(prop[0])
            elif type(prop[0][0]) in (float, int, bool, str):
                return prop[0][0]
            elif len(prop[0][0]) in [3, 4] and ("color" in key.lower() or is_color):  # in socket may be send color without alpha
                color = list(prop[0][0])
                return tuple(np.array([color[2], color[1], color[0]]) * 255)
            else:
                return prop[0][0]
        else:
            prop = getattr(self, key, None)
            if isinstance(prop, (int, float, bool, type(None))):
                return prop
            elif isinstance(prop, (str,)):
                return getattr(cv2, prop, prop)
            elif len(prop) == 4 and ("color" in key.lower() or is_color):
                color = list(prop)
                return tuple(np.array([color[2], color[1], color[0]]) * 255)
            else:
                return tuple(prop)

    def _get_sockets_by_socket_name(self, socket_name):
        if "_in" in socket_name:
            return self.inputs
        if "_out" in socket_name:
            return self.outputs

    def update_sockets_for_node_mode(self, props_maps, node_mode):
        for socket_name in list(chain(*props_maps.values())):
            sockets = self._get_sockets_by_socket_name(socket_name)
            if socket_name in sockets and socket_name not in props_maps[node_mode]:
                sockets.remove(sockets[socket_name])
        for prop_name in props_maps[node_mode]:
            sockets = self._get_sockets_by_socket_name(prop_name)
            if not prop_name in sockets:
                if self.is_uuid(getattr(self, prop_name)):
                    sockets.new('StringsSocket', prop_name)
                else:
                    sockets.new('StringsSocket', prop_name).prop_name = prop_name

    def get_kwargs_inputs(self, props_maps, input_mode):
        kwargs_inputs = {}
        for prop_name in props_maps[input_mode]:
            value = self.get_from_props(prop_name)
            if isinstance(value, list):
                value = tuple(value)
            kwargs_inputs[prop_name] = value
        return kwargs_inputs

    def check_input_requirements(self, requirements=None, optional=None):
        requirements = [] if requirements is None else requirements
        optional = [] if optional is None else optional
        for requirement in requirements:
            if requirement in optional:
                continue
            if not self.inputs[requirement].is_linked:
                self.use_custom_color = True
                self.color = NODE_COLOR_REQUIRE_DATE
                raise LackRequiredSocket("Inputs[{}] not linked".format(requirement))
        self.use_custom_color = False


    def check_inputs_requirements_mode(self, requirements=None, props_maps=None, input_mode=None):
        for requirement in requirements:
            if requirement[1] == input_mode:
                if not self.inputs[requirement[0]].is_linked:
                    raise LackRequiredSocket("Inputs[{}] not linked".format(requirement))

    def clean_kwargs(self, kwargs_in):
        kwargs_out = {}
        for key in kwargs_in.keys():
            value = kwargs_in.get(key)
            if IS_WORK_ON_COPY_INPUT and key in ("image_in", "img_in"):
                value = value.copy()

            if isinstance(value, (str,)) and value == "None":
                continue
            kwargs_out[key.replace("_in", "")] = value

        return kwargs_out

    def process(self):
        try:
            self.n_meta = ""
            start = time.time()
            self.wrapped_process()
            self.n_meta += "\nProcess time: {0:.2f}ms".format((time.time() - start) * 1000)
        except LackRequiredSocket as e:
            logger.info("SOCKET UNLINKED - {}".format(self))
            return

    def process_cv(self, fn=None, kwargs=None):
        kwargs = self.clean_kwargs(kwargs)
        try:
            start = time.time()
            out = fn(**kwargs)
            self.n_meta = "\nCV time: {0:.2f}ms".format((time.time() - start) * 1000)
        except Exception as e:
            logger.warngin("CV process problem: fn={}, kwargs={}, self={} ".format(fn, kwargs, self))
            raise
        return out

    def refresh_output_socket(self, prop_name=None, prop_value=None, is_uuid_type=False):
        if self.outputs[prop_name].is_linked:
            if is_uuid_type:
                _uuid = str(uuid.uuid4())
                setattr(self, prop_name, _uuid)
                self.socket_data_cache[_uuid] = prop_value
                self.outputs[prop_name].sv_set(_uuid)
            else:
                setattr(self, prop_name, prop_value)
                self.outputs[prop_name].sv_set([[prop_value]])

    def draw_buttons_ext(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        if getattr(self, 'bl_label', None) and getattr(cv2, self.bl_label, None):
            row.operator('wm.url_open', text="Documentation online - {}".format(self.bl_label), icon='URL').url = 'https://docs.opencv.org/3.0-last-rst/search.html?q={}&check_keywords=yes&area=default'.format(self.bl_label)
            row.operator('text.show_help_in_text_editor', text='Documentation docstring - {}'.format(self.bl_label), icon="TEXT").origin = self.get_node_origin()

        for msg in self.n_meta.split("\n"):
            layout.label(msg)

    def get_node_origin(self, props_name=None):
        node_tree = self.id_data.name
        node_name = self.name
        id_list = [node_tree, node_name]
        if props_name:
            if isinstance(props_name, str):
                props_name = props_name.split('|><|')
            for prop_name in props_name:
                id_list.append(prop_name)
        return '|><|'.join(id_list)

    def add_button(self, layout, prop_name, expand=False, toggle=False, icon=None, text=None):
        col = layout.column(align=True)
        row = col.row(align=True)

        kwargs = {}
        local_kwargs = locals()
        for kwarg_name in ["expand", "toggle", "icon", "text"]:
            if local_kwargs.get(kwarg_name):
                kwargs[kwarg_name] = local_kwargs.get(kwarg_name)

        row.prop(self, prop_name, **kwargs)

    def add_button_get_points(self, layout, props_name=None):
        if props_name and OCVL_EXT:
            row = layout.row()
            col = layout.column(align=True)
            origin = self.get_node_origin(props_name="|><|".join(props_name))
            col.operator('image.point_select', text=', '.join(props_name), icon="CURSOR").origin = origin


class OCVLPreviewNode(OCVLNode):
    texture = {}

    def delete_texture(self):
        if self.node_id in self.texture:
            bgl.glDeleteTextures(2, bgl.Buffer(bgl.GL_INT, 2, self.texture[self.node_id]["name"]))

    def free(self):
        nvBGL2.callback_disable(node_id(self))
        self.delete_texture()

    def make_textures(self, image, color='RGBA', uuid_=None, width=200, height=200):
        self.delete_texture()

        height_, width_ = image.shape[:2]

        prop = height_ / width_

        resized_image = cv2.resize(image, (width, int(height * prop)))
        resized_height, resized_width = resized_image.shape[:2]

        texture_mini = bgl.Buffer(bgl.GL_BYTE, resized_image.shape, resized_image)

        name = bgl.Buffer(bgl.GL_INT, 2)
        bgl.glGenTextures(2, name)
        self.texture[self.node_id] = {"name": name, "uuid": uuid_}
        self.texture[uuid_] = self.node_id
        if len(image.shape) == 3:
            internalFormat = bgl.GL_RGB
            format = bgl.GL_BGR
        elif len(image.shape) == 2:
            internalFormat = bgl.GL_LUMINANCE
            format = bgl.GL_LUMINANCE
        init_texture(width=resized_width,
                     height=resized_height,
                     texname=name[1],
                     texture=texture_mini,
                     internalFormat=internalFormat,
                     format=format)

    def draw_preview(self, layout, prop_name="image_out", location_x=0, location_y=0):
        row = layout.row()
        row.label(text='')

        if self.n_id not in self.texture:
            return
        nvBGL2.callback_disable(self.n_id)
        image = self.get_from_props(prop_name)
        height, width = image.shape[:2]
        prop = height / width
        SCALE = bpy.context.user_preferences.system.pixel_size

        width = (self.width - 20) * SCALE
        height = prop * width
        row.scale_y = self.width * prop / 20

        self._draw_preview(prop_name="image_out", location_x=location_x, location_y=location_y, width=width, height=height)

    def _draw_preview(self, prop_name="image_out", location_x=0, location_y=0, width=0, height=0, hide=False):
        nvBGL2.callback_disable(self.n_id)

        draw_data = {
            'tree_name': self.id_data.name,
            'mode': 'custom_function',
            'custom_function': simple_screen,
            'loc': (self.location[0] + location_x, self.location[1] + location_y - self.height),
            'args': (None,
                     self.texture[self.n_id]["name"][1],
                     width,
                     height,
                     getattr(self, 'r_in', 1),
                     getattr(self, 'g_in', 1),
                     getattr(self, 'b_in', 1),
                     0 if hide else 1,
                     TEX_CO_FLIP,
                     )
            }

        nvBGL2.callback_enable(self.n_id, draw_data)


def cv_register_class(cls):
    if cls.__name__.endswith("Node"):
        cls.n_id = StringProperty(default='')
        cls.n_meta = StringProperty(default='')
        cls.bl_idname = cls.__name__
        cls.bl_label = getattr(cls, 'bl_label', cls.bl_idname[4:-4])
        cls.bl_icon = 'OUTLINER_OB_EMPTY'

    try:
        bpy.utils.register_class(cls)
        logger.debug("Cass registrated: {}".format(cls))
    except ValueError as e:
        logger.warning(e)
        logger.warning("Class {} already registered".format(cls))


def cv_unregister_class(cls):
    try:
        bpy.utils.unregister_class(cls)
    except RuntimeError as e:
        logger.warning(e)
        logger.warning("Class {} problem with unregister".format(cls))
