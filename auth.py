from collections import OrderedDict
from os.path import dirname
from urllib import parse
import logging
import json
import bpy
import os


from . import bl_info

logger = logging.getLogger(__name__)

ANONYMOUS = "Anonymous"
COMMUNITY_VERSION = "COMMUNITY_VERSION"
PRO_VERSION = "PRO_VERSION"

OCVL_PANEL_URL = "http://127.0.0.1:5000/"
OCVL_GITHUB_ISSUE_TEMPLATE = "https://github.com/feler404/ocvl-addon/issues/new?title={title}&body={body}"
OCVL_VERSION = ".".join(map(str, bl_info['version']))
OCVL_EXT_VERSION = OCVL_VERSION
OCVL_AUTH_PARAMS_BASE_TEMPALTE = "?&ocvl_version={}&ocvl_ext_version={}".format(OCVL_VERSION, OCVL_EXT_VERSION)
OCVL_AUTH_PARAMS_LOGIN_PASSWORD_TEMPALTE = OCVL_AUTH_PARAMS_BASE_TEMPALTE + "&login={login}&password={password}"
OCVL_AUTH_PARAMS_LICENCE_KEY_TEMPALTE = OCVL_AUTH_PARAMS_BASE_TEMPALTE + "&licence_key={licence_key}"
OCVL_EXTENDED_NODE_PREFIX = "Ext-"
OCVL_SIMPLE_NODE_PREFIX = "Simple-"

OCVL_LINK_UPGRADE_PROGRAM_TO_PRO = 'https://ocvl-cms.herokuapp.com/admin/login/'
OCVL_LINK_TO_OCVL_PANEL = 'https://ocvl-cms.herokuapp.com/admin/login/'
OCVL_LINK_TO_STORE = 'http://kube.pl/'
OCVL_LINK_TO_CREATE_ACCOUNT = 'http://kube.pl/'


class Auth:

    _ocvl_version = COMMUNITY_VERSION
    _ocvl_version = PRO_VERSION
    _ocvl_ext = None
    _ocvl_first_running = True
    _ocvl_pro_version_auth = False
    _ocvl_pro_version_auth = True

    instance = None

    def __new__(cls):
        if not Auth.instance:
            Auth.instance = object.__new__(cls)
        return Auth.instance

    @property
    def ocvl_version(self):
        return self._ocvl_version

    @property
    def ocvl_first_running(self):
        return self._ocvl_first_running

    @property
    def ocvl_ext(self):
        if self._ocvl_ext is None:
            try:
                from .extend.extended_utils import OCLV_EXTEND_MODULE_FAKE_VAR
                self._ocvl_ext = True
            except:
                self._ocvl_ext = False
        else:
            return self._ocvl_ext

    @property
    def ocvl_pro_version_auth(self):
        return self._ocvl_pro_version_auth

    def set_attr_auth(self, name, value, key=None):
        setattr(self, "_{}".format(name), value)

    @property
    def viewer_name(self):
        if self.ocvl_version == COMMUNITY_VERSION:
            return "OCVLSimpleImageViewerNode"
        elif self.ocvl_version == PRO_VERSION:
            return "OCVLImageViewerNode"



class User:

    instance = None
    auth = None
    name = ANONYMOUS
    tutorials = [{"name": "First steps",
                  "icon": "PARTICLE_DATA",
                  "purchase_time": None,
                  "content": "<html>Tut</html>"
                }]
    assets = []

    def __new__(cls, *args, **kwargs):
        if not User.instance:
            User.instance = object.__new__(cls)
        return User.instance

    def __init__(self, auth):
        self.auth = auth

    @property
    def is_login(self):
        return self.name != ANONYMOUS


ocvl_auth = Auth()
ocvl_user = User(ocvl_auth)


def auth_pro_confirm(node, url, response):
    if response.status_code == 200:
        node.auth = True
        ocvl_auth.set_attr_auth("ocvl_pro_version_auth", True)
        ocvl_user.name = "Dawid"
        logger.info("Authentication confirm for {}".format(ocvl_user.name))

        content = response.json()
        ocvl_user.tutorials.extend(content.get("tutorials", []))
        ocvl_user.assets = content.get("assets", [])
        logger.info("Content payload {} for user {}".format(content, ocvl_user.name))
        from .sverchok_point import soft_reload_menu
        soft_reload_menu()


def auth_pro_reject(node, url, response):
    parsed = parse.urlparse(url)
    ocvl_user.name = str(parse.parse_qs(parsed.query).get('login', [ANONYMOUS])[0])
    logger.info("Authentication rejected for {}".format(ocvl_user.name))


def register_extended_operators():
    if ocvl_auth.ocvl_ext:
        from .extend.extended_operatores import register; register()


def unregister_extended_operators():
    if ocvl_auth.ocvl_ext:
        from .extend.extended_operatores import unregister; unregister()


def auth_make_node_cats_new():
    '''
    this loads the index.md file and converts it to an OrderedDict of node categories.

    '''
    index_path = os.path.join(dirname(__file__), 'index.md')

    node_cats = OrderedDict()
    with open(index_path) as md:
        category = None
        temp_list = []
        for line in md:
            if not line.strip():
                continue
            if line.strip().startswith('>'):
                continue
            elif line.startswith('##'):
                if category:
                    node_cats[category] = temp_list
                category = line[2:].strip()
                temp_list = []

            elif line.strip() == '---':
                temp_list.append(['separator'])
            else:
                bl_idname = line.strip()
                extended_node = False
                simple_node = False
                if bl_idname.startswith(OCVL_EXTENDED_NODE_PREFIX):
                    extended_node = True
                    bl_idname = bl_idname.replace(OCVL_EXTENDED_NODE_PREFIX, "")
                if bl_idname.startswith(OCVL_SIMPLE_NODE_PREFIX):
                    simple_node = True
                    bl_idname = bl_idname.replace(OCVL_SIMPLE_NODE_PREFIX, "")
                if (not ocvl_auth.ocvl_ext) or (not ocvl_auth.ocvl_pro_version_auth):
                    if extended_node:
                        continue
                elif simple_node:
                    continue

                temp_list.append([bl_idname])

        # final append
        node_cats[category] = temp_list

    return node_cats
