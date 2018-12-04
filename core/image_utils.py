import cv2
import bpy
import gpu
import bgl
import numpy as np
from gpu_extras.batch import batch_for_shader

from ocvl.core.globals import CALLBACK_DICT


def tag_redraw_all_nodeviews():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'NODE_EDITOR':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        region.tag_redraw()


def simple_screen(image, x, y, width, height):
    if image.gl_load():
        raise Exception()
    bgl.glActiveTexture(bgl.GL_TEXTURE0)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, image.bindcode)

    shader = gpu.shader.from_builtin('2D_IMAGE')
    batch = batch_for_shader(
        shader, 'TRI_FAN',
        {
            "pos": ((x, y), (x+width, y), (x+width, y+height), (x, y+height)),
            "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
        },
    )

    shader.bind()
    shader.uniform_int("image", 0)
    batch.draw(shader)


def callback_enable(n_id=None, image=None, x=None, y=None, width=None, height=None):
    if n_id in CALLBACK_DICT:
        return

    args = image, x, y, width, height
    handle_pixel = bpy.types.SpaceNodeEditor.draw_handler_add(simple_screen, args, 'WINDOW', 'POST_VIEW')
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
    bgl.glTexParameterf(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_S, bgl.GL_CLAMP_TO_EDGE)  # bgl.GL_CLAMP
    bgl.glTexParameterf(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_T, bgl.GL_CLAMP_TO_EDGE)  # bgl.GL_CLAMP
    bgl.glTexParameterf(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_LINEAR)
    bgl.glTexParameterf(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_LINEAR)
    bgl.glTexImage2D(
        bgl.GL_TEXTURE_2D,
        0, internalFormat, width, height,
        0, format, bgl.GL_UNSIGNED_BYTE, texture
    )


def convert_to_cv_image(image_gl):
    image_cv = np.array(image_gl.pixels, dtype=np.float32)
    image_cv = image_cv.reshape((image_gl.size[1], image_gl.size[0], image_gl.channels))
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGBA2BGR) * 255
    image_cv = cv2.flip(image_cv, 0)
    image_cv.astype(np.uint8)
    return image_cv
