from contextlib import contextmanager

import bpy
import sys

from io import StringIO
from tornado import web
from logging import getLogger

from tornado.escape import json_encode

from .settings import (
    TUTORIAL_ENGINE_VERSION, TUTORIAL_ENGINE_DEFAULT_NODE_TREE_NAME,
    TUTORIAL_ENGINE_DEFAULT_IMAGE_SAMPLE_NAME,
    TUTORIAL_ENGINE_DEFAULT_VIEWER_NAME,
    TUTORIAL_ENGINE_DEFAULT_INPUT_NAME,
    TUTORIAL_ENGINE_DEFAULT_OUTPUT_NAME,
)

logger = getLogger(__name__)


class BaseHandler(web.RequestHandler):

    def delist_arguments(self, args):
        """
        Takes a dictionary, 'args' and de-lists any single-item lists then
        returns the resulting dictionary.

        In other words, {'foo': ['bar']} would become {'foo': 'bar'}
        """
        for arg, value in args.items():
            if len(value) == 1:
                if isinstance(value[0], bytes):
                    args[arg] = value[0].decode()
                else:
                    args[arg] = value[0]
        return args

    def get_kwargs(self):
        kwargs = {}
        if self.request.arguments:
            kwargs = self.delist_arguments(self.request.arguments)
        return kwargs

    def reply(self, data):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.finish(json_encode(data))


class Error404Handler(BaseHandler):

    @staticmethod
    def get(self):
        raise web.HTTPError(404)


class IndexHandler(BaseHandler):
    """
    IndexHandler - Welcome Page
    """

    def get(self):
        resp = {"status_code": 200, "msg": "Tutorial Engine Server working - {}".format(TUTORIAL_ENGINE_VERSION)}
        self.reply(resp)


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


def run_cam(command=""):

    with Capturing() as output:
        try:
            ret = exec("print({})".format(command))
            status_code = 200
        except (TypeError, SyntaxError) as e:
            try:
                var = command.split("=")[0]
                ret = exec("{}".format(command))
                status_code = 200
                try:
                    exec("print('{}')".format(var))
                    exec("print({})".format(var))
                except SyntaxError as e:
                    logger.info("Evaluation syntax skip: {}".format(e))
            except Exception as e:
                ret = e, type(e)
                status_code = 501
        except Exception as e:
            ret = e, type(e)
            status_code = 502
    if status_code > 500:
        output = []
        ret = str(ret)
    return {"command": command,
            "status_code": status_code,
            "output": output,
            "ret": ret}


@contextmanager
def in_node_context():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'NODE_EDITOR':
                override = {'window': window, 'screen': screen, 'area': area}
                yield override
                break


class RawCommandHandler(BaseHandler):
    """
    IndexHandler - Welcome Page
    """

    def get(self, *args):
        kwargs = self.get_kwargs()
        command = kwargs.get("command", "")
        logger.info("Raw command prepare: {}".format(command))
        resp = run_cam(command)
        # resp = {"command": command, "status_code": 200}
        self.reply(resp)


class NodeCommandHandler(BaseHandler):
    """
    IndexHandler - Welcome Page
    """

    @classmethod
    def clear_node_groups(cls):
        for node_group_name, node_group in bpy.data.node_groups.items():
            bpy.data.node_groups.remove(node_group)

    @classmethod
    def view_all(cls):
        with in_node_context() as override:
            bpy.ops.node.view_all(override)

    @classmethod
    def get_or_create_node_tree(cls, name=TUTORIAL_ENGINE_DEFAULT_NODE_TREE_NAME):
        if TUTORIAL_ENGINE_DEFAULT_NODE_TREE_NAME not in bpy.data.node_groups:
            with in_node_context() as override:
                bpy.ops.node.new_node_tree(override, name=name)
        return bpy.data.node_groups[TUTORIAL_ENGINE_DEFAULT_NODE_TREE_NAME]

    @classmethod
    def get_or_create_default_image_sample(cls):
        node_tree = cls.get_or_create_node_tree()
        node = node_tree.nodes.get(TUTORIAL_ENGINE_DEFAULT_IMAGE_SAMPLE_NAME)
        if not node:
            node = node_tree.nodes.new(TUTORIAL_ENGINE_DEFAULT_IMAGE_SAMPLE_NAME)
        node.location = (0, 0)
        return node

    @classmethod
    def get_or_create_default_viewer(cls):
        node_tree = cls.get_or_create_node_tree()
        node = node_tree.nodes.get(TUTORIAL_ENGINE_DEFAULT_VIEWER_NAME)
        if not node:
            node = node_tree.nodes.new(TUTORIAL_ENGINE_DEFAULT_VIEWER_NAME)
        node.location = (300, 0)
        return node

    @classmethod
    def connect_nodes(cls,
                      node_input=TUTORIAL_ENGINE_DEFAULT_VIEWER_NAME,
                      input_name=TUTORIAL_ENGINE_DEFAULT_INPUT_NAME,
                      node_output=TUTORIAL_ENGINE_DEFAULT_IMAGE_SAMPLE_NAME,
                      output_name=TUTORIAL_ENGINE_DEFAULT_OUTPUT_NAME):

        node_tree = cls.get_or_create_node_tree()
        socket_input = node_tree.nodes[node_input].inputs[input_name]
        socket_output = node_tree.nodes[node_output].outputs[output_name]
        node_tree.links.new(socket_input, socket_output)

    @classmethod
    def change(cls, node_name, prop_name, value):
        node_tree = cls.get_or_create_node_tree()
        node = node_tree.nodes.get(node_name)
        setattr(node,prop_name, eval(value))


    def get(self, *args):
        kwargs = self.get_kwargs()
        command = kwargs.pop("command", "")
        bpy.worker_queue.append({"command": command, "kwargs": kwargs})

        logger.info("Raw command prepare: {}".format(command))
        # resp = run_cam(command)
        resp = {"command": command, "status_code": 200}
        self.reply(resp)


def tutorial_engine_app():
    return web.Application([
        (r"/", IndexHandler),
        (r"/node/.*", NodeCommandHandler),
        (r"/raw/.*", RawCommandHandler),
        (r"/.*", Error404Handler),

    ],
        debug=True,
        autoreload=True
    )