# Color node without necessary data to process
import os

NODE_COLOR_REQUIRE_DATE = (1, 0.3, 0)
# Color node with CV error
NODE_COLOR_CV_ERROR = (0.6, 0.0, 0.0)
# In draw_buttons_ext width text
WRAP_TEXT_SIZE_FOR_ERROR_DISPLAY = 75
# In NodeBase if True make copy for "image_in/img_in" sockets data
IS_WORK_ON_COPY_INPUT = True
# Category nodes which don't should appear in interface
BLACK_LIST_REGISTER_NODE_CATEGORY = ["__pycache__", "interface", "TODO"]
# Max number lines displayed on Stethoscope node
STETHOSCOPE_NODE_MAX_LINES = 30
# Default filter during use ocvl.ocvl_image_importer operator
DEFAULT_IMAGE_IMPORTER_FILTER = "*.tif;*.png;*.jpeg;*.jpg"

DEBUG_MODE = os.environ.get("OCVL_DEBUG", False)
DEBUG = DEBUG_MODE

class Category:
    uncategorized = "uncategorized"
    filters = "filters"


class SocketColors:
    OCVLMatrixSocket = 0.1, 1.0, 0.2, 1
    OCVLColorSocket = 0.1, 0.7, 1.0, 1
    OCVLImageSocket = 0.1, 1.0, 0.8, 1
    OCVLMaskSocket = 0.0, 0.0, 0.0, 1
    OCVLRectSocket = 0.2, 0.4, 0.4, 1
    OCVLContourSocket = 0.2, 0.8, 1.0, 1
    OCVLVectorSocket = 0.1, 1.0, 0.2, 1
    OCVLStethoscopeSocket = 1.0, 1.0, 1.0, 1


CATEGORY_TREE = Category()
SOCKET_COLORS = SocketColors()

# Maximum value for float number from sys.float_info.max
DBL_MAX = 1.7976931348623156e+308

DEFAULT_NODE_FOR_QUICK_LINK_IMAGE_SOCKET = os.environ.get("DEFAULT_NODE_FOR_QUICK_LINK_IMAGE_SOCKET", "OCVLImageSampleNode")
DEFAULT_NODE_FOR_QUICK_LINK_MASK_SOCKET = "OCVLMaskSampleNode"
DEFAULT_NODE_FOR_QUICK_LINK_RECT_SOCKET = "OCVLRectNode"
DEFAULT_NODE_FOR_QUICK_LINK_CONTOUR_SOCKET = "OCVLfindContoursNode"
DEFAULT_NODE_FOR_QUICK_LINK_VECTOR_SOCKET = "OCVLVecNode"

DEFAULT_NODE_FOR_QUICK_LINK_IMAGE_SOCKET_OUT = os.environ.get("DEFAULT_NODE_FOR_QUICK_LINK_IMAGE_SOCKET_OUT", "OCVLImageViewerNode")

DEFAULT_QUICK_LINK_LOCATION_X_OFFSET = 40
DEFAULT_QUICK_LINK_LOCATION_Y_OFFSET = -10
DEFAULT_QUICK_LINK_LOCATION_Y_OFFSET_FIRST_NODE = 50
