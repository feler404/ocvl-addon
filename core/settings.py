# Color node without necessary data to process
import os


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
# Debug flag if on display in log many additional information
DEBUG = os.environ.get("OCVL_DEBUG", False)
# Maximum value for float number from sys.float_info.max
DBL_MAX = 1.7976931348623156e+308


##################################################
# Color section ###
##################################################
SOCKET_COLORS = {
    "OCVLObjectSocket": (0.1, 1.0, 0.2, 1),
    "OCVLColorSocket": (0.1, 0.7, 1.0, 1),
    "OCVLImageSocket":  (0.1, 1.0, 0.8, 1),
    "OCVLMaskSocket": (0.0, 0.0, 0.0, 1),
    "OCVLRectSocket": (0.2, 0.4, 0.4, 1),
    "OCVLContourSocket": (0.2, 0.8, 1.0, 1),
    "OCVLVectorSocket": (0.1, 1.0, 0.2, 1),
    "OCVLStethoscopeSocket": (1.0, 1.0, 1.0, 1),
}
# Color node without data
NODE_COLOR_REQUIRE_DATE = (1, 0.3, 0)
# Color node with CV error
NODE_COLOR_CV_ERROR = (0.6, 0.0, 0.0)

##################################################
# Quick link settings ###
##################################################
DEFAULT_NODE_FOR_QUICK_LINK_IMAGE_SOCKET = os.environ.get("DEFAULT_NODE_FOR_QUICK_LINK_IMAGE_SOCKET", "OCVLImageSampleNode")
DEFAULT_NODE_FOR_QUICK_LINK_MASK_SOCKET = "OCVLMaskSampleNode"
DEFAULT_NODE_FOR_QUICK_LINK_RECT_SOCKET = "OCVLRectNode"
DEFAULT_NODE_FOR_QUICK_LINK_CONTOUR_SOCKET = "OCVLfindContoursNode"
DEFAULT_NODE_FOR_QUICK_LINK_VECTOR_SOCKET = "OCVLVecNode"

DEFAULT_NODE_FOR_QUICK_LINK_IMAGE_SOCKET_OUT = os.environ.get("DEFAULT_NODE_FOR_QUICK_LINK_IMAGE_SOCKET_OUT", "OCVLImageViewerNode")

DEFAULT_QUICK_LINK_LOCATION_X_OFFSET = 40
DEFAULT_QUICK_LINK_LOCATION_Y_OFFSET = -10
DEFAULT_QUICK_LINK_LOCATION_Y_OFFSET_FIRST_NODE = 50

##################################################
# Node tree registration section ###
##################################################
OCVL_NODE_CATEGORIES = "OCVLCategories"
OCVL_NODE_TREE_TYPE = "OCVLGroupTreeType"
OCVL_PRO_DIR_NAME = "ocvl_addon_pro"

PREFIX_NODE_CLASS = "OCVL"
SUFFIX_NODE_CLASS = "Node"
BLACK_LIST_FOR_REGISTER_NODE = ["OCVLNode", "OCVLPreviewNode"]
ID_TREE_CATEGORY_TEMPLATE = "OCVL_CATEGORY_{}"
NAME_NODE_DIRECTORY = "nodes"

##################################################
# Common settings for nodes definitions ###
##################################################
MAP_NUMPY_CTYPES_OPENCV_CTYPES = {
    "float32": "CV_32F",
    "float64": "CV_64F",
}

NP_VALUE_TYPE_ITEMS = (
    # ("NONE", "NONE", "NONE", "", 0),
    # ("intc", "intc", "intc", "", 1),
    # ("intp", "intp", "intp", "", 2),
    # ("int8", "int8", "int8", "", 3),
    # ("int16", "int16", "int16", "", 4),
    # ("int32", "int32", "int32", "", 5),
    # ("int64", "int64", "int64", "", 6),
    ("uint8", "uint8", "uint8", "", 0),
    ("uint16", "uint16", "uint16", "", 1),
    # ("uint32", "uint32", "uint32", "", 2),
    # ("uint64", "uint64", "uint64", "", 10),
    # ("float16", "float16", "float16", "", 3),
    ("float32", "float32", "float32", "", 2),
    # ("float64", "float64", "float64", "", 13),
)
