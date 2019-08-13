import bpy
from bpy.app.handlers import persistent


@persistent
def refresh_after_load(*args):

    try:
        node_groups = bpy.data.node_groups
    except AttributeError as e:
        return

    for node_group in node_groups:
        for node in node_group.nodes:
            node.process()


def register(settings):
    if not refresh_after_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(refresh_after_load)


def unregister(settings):
    if refresh_after_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(refresh_after_load)