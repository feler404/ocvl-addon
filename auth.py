from urllib import parse
import logging
from . import bl_info

logger = logging.getLogger(__name__)

ANONYMOUS = "Anonymous"
COMMUNITY_VERSION = "COMMUNITY_VERSION"
PRO_VERSION = "PRO_VERSION"
OCVL_PANEL_URL = "http://127.0.0.1:5000/"
OCVL_GITHUB_ISSUE_TEMPLATE = "https://github.com/feler404/ocvl-addon/issues/new?title={title}&body={body}"
OCVL_VERSION = bl_info['version']


class Auth:

    COMMUNITY_VERSION = COMMUNITY_VERSION
    PRO_VERSION = PRO_VERSION
    OCVL_PANEL_URL = OCVL_PANEL_URL

    _ocvl_version = PRO_VERSION
    _ocvl_first_running = True
    _ocvl_ext = False
    _ocvl_pro_version_auth = False

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
        return self._ocvl_ext

    @property
    def ocvl_pro_version_auth(self):
        return self._ocvl_pro_version_auth

    def set_attr_auth(self, name, value, key=None):
        setattr(self, "_{}".format(name), value)


class User:

    instance = None
    auth = None
    name = ANONYMOUS

    def __new__(cls, *args, **kwargs):
        if not User.instance:
            User.instance = object.__new__(cls)
        return User.instance

    def __init__(self, auth):
        self.auth = auth


ocvl_auth = Auth()
ocvl_user = User(ocvl_auth)


def auth_pro_confirm(node, url, response):
    if response.status_code == 200:
        node.auth = True
        ocvl_auth.set_attr_auth("ocvl_pro_version_auth", True)
        ocvl_user.name = "Dawid"
        logger.info("Authentication confirm")


def auth_pro_reject(node, url, response):
    parsed = parse.urlparse(url)
    ocvl_user.name = str(parse.parse_qs(parsed.query).get('login', [ANONYMOUS])[0])
    logger.info("Authentication rejected for {}".format(ocvl_user.name))