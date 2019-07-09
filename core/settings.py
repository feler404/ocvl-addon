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
# Max number lines displayed on Stethoscope node
STETHOSCOPE_NODE_MAX_LINES = 30
# Default filter during use image.ocvl_image_importer operator
DEFAULT_IMAGE_IMPORTER_FILTER = "*.tif;*.png;*.jpeg;*.jpg"

DEBUG_MODE = False
DEBUG = DEBUG_MODE

class Category:
    uncategorized = "uncategorized"
    filters = "filters"


class SocketColors:
    StringsSocket = 0.1, 1.0, 0.2, 1
    SvColorSocket = 0.1, 0.7, 1.0, 1
    ImageSocket = 0.1, 1.0, 0.8, 1
    MaskSocket = 0.0, 0.0, 0.0, 1
    RectSocket = 0.2, 0.4, 0.4, 1
    ContourSocket = 0.2, 0.8, 1.0, 1
    VectorSocket = 0.1, 1.0, 0.2, 1
    StethoscopeSocket = 1.0, 1.0, 1.0, 1


CATEGORY_TREE = Category()
SOCKET_COLORS = SocketColors()

# Maximum value for float number from sys.float_info.max
DBL_MAX = 1.7976931348623156e+308