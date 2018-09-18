from collections import defaultdict

import cv2
import bgl
import bpy
import blf
import numpy as np
from ocvl.core.node_tree import OCVLNodeTree
from ocvl.globals import CALLBACK_DICT

TEX_CO = [(0, 1), (1, 1), (1, 0), (0, 0)]
TEX_CO_FLIP = [(0, 0), (1, 0), (1, 1), (0, 1)]


def tag_redraw_all_nodeviews():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'NODE_EDITOR':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        region.tag_redraw()


def restore_opengl_defaults():
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


def draw_text_data(data):
    lines = data.get('content', 'no data')
    x, y = data.get('location', (120, 120))
    x, y = int(x), int(y)
    color = data.get('color', (0.1, 0.1, 0.1))
    font_id = data.get('font_id', 0)
    scale = data.get('scale', 1.0)

    text_height = 15 * scale
    line_height = 14 * scale

    # why does the text look so jagged?  <-- still valid question
    # dpi = bpy.context.user_preferences.system.dpi
    blf.size(font_id, int(text_height), 72)
    bgl.glColor3f(*color)
    ypos = y

    for line in lines:
        blf.position(0, x, ypos, 0)
        blf.draw(font_id, line)
        ypos -= int(line_height * 1.3)


def draw_graphical_data(data):
    lines = data.get('content')
    x, y = data.get('location', (120, 120))
    color = data.get('color', (0.1, 0.1, 0.1))
    font_id = data.get('font_id', 0)
    scale = data.get('scale', 1.0)
    text_height = 15 * scale

    if not lines:
        return

    blf.size(font_id, int(text_height), 72)

    def draw_text(color, xpos, ypos, line):
        bgl.glColor3f(*color)
        blf.position(0, xpos, ypos, 0)
        blf.draw(font_id, line)
        return blf.dimensions(font_id, line)

    lineheight = 20 * scale
    num_containers = len(lines)
    for idx, line in enumerate(lines):
        y_pos = y - (idx * lineheight)
        gfx_x = x

        num_items = str(len(line))
        kind_of_item = type(line).__name__

        tx, _ = draw_text(color, gfx_x, y_pos, "{0} of {1} items".format(kind_of_item, num_items))
        gfx_x += (tx + 5)

        content_dict = defaultdict(int)
        for item in line:
            content_dict[type(item).__name__] += 1

        tx, _ = draw_text(color, gfx_x, y_pos, str(dict(content_dict)))
        gfx_x += (tx + 5)

        if idx == 19 and num_containers > 20:
            y_pos = y - ((idx + 1) * lineheight)
            text_body = "Showing the first 20 of {0} items"
            draw_text(color, x, y_pos, text_body.format(num_containers))
            break


def draw_callback_px(n_id, data):
    space = bpy.context.space_data

    ng_view = space.edit_tree
    # ng_view can be None
    if not ng_view:
        return
    ng_name = space.edit_tree.name
    if not (data['tree_name'] == ng_name):
        return
    if not isinstance(ng_view, OCVLNodeTree):
        return

    if data.get('mode', 'text-based') == 'text-based':
        draw_text_data(data)
    elif data.get('mode') == "graphical":
        draw_graphical_data(data)
        restore_opengl_defaults()
    elif data.get('mode') == 'custom_function':
        drawing_func = data.get('custom_function')
        x, y = data.get('loc', (20, 20))
        args = data.get('args', (None,))
        drawing_func(x, y, args)
        restore_opengl_defaults()


def callback_enable(*args):
    n_id = args[0]
    if n_id in CALLBACK_DICT:
        return

    handle_pixel = bpy.types.SpaceNodeEditor.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_VIEW')
    CALLBACK_DICT[n_id] = handle_pixel
    tag_redraw_all_nodeviews()


def callback_disable(n_id):
    handle_pixel = CALLBACK_DICT.get(n_id, None)
    if not handle_pixel:
        return
    bpy.types.SpaceNodeEditor.draw_handler_remove(handle_pixel, 'WINDOW')
    del CALLBACK_DICT[n_id]
    tag_redraw_all_nodeviews()


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


def convert_to_cv_image(image_gl):
    image_cv = np.array(image_gl.pixels, dtype=np.float32)
    image_cv = image_cv.reshape((image_gl.size[1], image_gl.size[0], image_gl.channels))
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGBA2BGR) * 255
    image_cv = cv2.flip(image_cv, 0)
    image_cv.astype(np.uint8)
    return image_cv
