from copy import deepcopy

import bpy
from ocvl.core.exceptions import NoDataError
from ocvl.globals import SOCKET_DATA_CACHE
from ocvl.core.register_utils import ocvl_register, ocvl_unregister


def set_socket(socket, out):
    """sets socket data for socket"""
    # if data_structure.DEBUG_MODE:
    #     if not socket.is_output:
    #         warning("{} setting input socket: {}".format(socket.node.name, socket.name))
    #     if not socket.is_linked:
    #         warning("{} setting unconncted socket: {}".format(socket.node.name, socket.name))
    s_id = socket.socket_id
    s_ng = socket.id_data.name
    if s_ng not in SOCKET_DATA_CACHE:
        SOCKET_DATA_CACHE[s_ng] = {}
    SOCKET_DATA_CACHE[s_ng][s_id] = out


def get_socket(socket, deepcopy_=True):
    """gets socket data from socket,
    if deep copy is True a deep copy is make_dep_dict,
    to increase performance if the node doesn't mutate input
    set to False and increase performance substanstilly
    """
    if socket.is_linked:
        other = socket.other
        s_id = other.socket_id
        s_ng = other.id_data.name
        if s_ng not in SOCKET_DATA_CACHE:
            raise LookupError
        if s_id in SOCKET_DATA_CACHE[s_ng]:
            out = SOCKET_DATA_CACHE[s_ng][s_id]
            if deepcopy_:
                return deepcopy(out)
            else:
                return out
        else:
            # if data_structure.DEBUG_MODE:
            #     debug("cache miss: %s -> %s from: %s -> %s",
            #             socket.node.name, socket.name, other.node.name, other.name)
            raise NoDataError(socket)
    # not linked
    raise NoDataError(socket)


class OCVLSocket(bpy.types.NodeSocket):

    @property
    def socket_id(self):
        return str(hash(self.id_data.name + self.node.name + self.identifier))

    def sv_set(self, data):
        set_socket(self, data)


    def sv_get(self, data):
        get_socket(self, data)


class OCVLUUIDSocket(OCVLSocket):
    '''Renderman co-shader input/output'''
    bl_idname = 'OCVLUUIDSocket'
    bl_label = 'OCVLUUIDSocket'

    uuid = bpy.props.StringProperty(default="")

    # Optional function for drawing the socket input value
    def draw_value(self, context, layout, node):
        layout.label(self.name)

    def draw_color(self, context, node):
        return (0.1, 1.0, 0.2, 1)

    def draw(self, context, layout, node, text):
        layout.label(text)
        pass


def register():
    ocvl_register(OCVLUUIDSocket)


def unregister():
    ocvl_unregister(OCVLUUIDSocket)
