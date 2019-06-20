# Color node without necessary data to process
NODE_COLOR_REQUIRE_DATE = (1, 0.3, 0)
# Color node with CV error
NODE_COLOR_CV_ERROR = (0.6, 0.0, 0.0)
# In draw_buttons_ext width text
WRAP_TEXT_SIZE_FOR_ERROR_DISPLAY = 75
# In NodeBase if True make copy for "image_in/img_in" sockets data
IS_WORK_ON_COPY_INPUT = True
# Category nodes which don't should appear in interface
BLACK_LIST_REGISTER_NODE_CATEGORY = ["interface"]

DEBUG_MODE = False
DEBUG = DEBUG_MODE

class Category:
    uncategorized = "uncategorized"
    filters = "filters"


class SocketColors:
    StringsSocket = 0.1, 1.0, 0.2, 1
    ImageSocket = 0.1, 1.0, 0.8, 1
    SvColorSocket = 0.1, 0.7, 1.0, 1


CATEGORY_TREE = Category()
SOCKET_COLORS = SocketColors()
