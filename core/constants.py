"""
Module to keep constance.
Example: constance names, math constance, gl constance
Example not: globals variables, settings
"""

OCVL_NODE_CATEGORIES = "OCVLCategories"
OCVL_NODE_TREE_TYPE = "OCVLGroupTreeType"

TEX_CO = [(0, 1), (1, 1), (1, 0), (0, 0)]
TEX_CO_FLIP = [(0, 0), (1, 0), (1, 1), (0, 1)]

PREFIX_NODE_CLASS = "OCVL"
SUFFIX_NODE_CLASS = "Node"
BLACKLIST_FOR_REGISTER_NODE = ["OCVLNode", "OCVLPreviewNode"]
ID_TREE_CATEGORY_TEMPLATE = "OCVL_CATEGORY_{}"
NAME_NODE_DIRECTORY = "nodes"

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
