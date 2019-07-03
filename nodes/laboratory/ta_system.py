import uuid

import bpy
import cv2
from ocvl.core.node_base import OCVLNodeBase, update_node


MACROS_ITEMS = (
    ("getBuildInformation", "getBuildInformation", "Returns full configuration time cmake output.", "", 0),
    ("checkHardwareSupport", "checkHardwareSupport", "Returns true if the specified feature is supported by the host hardware.", "", 1),
    ("getNumberOfCPUs", "getNumberOfCPUs", "Returns the number of logical CPUs available for the process.", "", 2),
    ("getNumThreads", "getNumThreads", "Returns the number of threads used by OpenCV for parallel regions. Always returns 1 if OpenCV is built without threading support.", "", 3),
    ("getThreadNum", "getThreadNum", "Returns the index of the currently executed thread within the current parallel region. Always returns 0 if called outside of parallel region.", "", 4),
    ("getTickCount", "getTickCount", "Returns the number of ticks.", "", 5),
    ("getTickFrequency", "getTickFrequency", "Returns the number of ticks per second.", "", 6),
    ("getCPUTickCount", "getCPUTickCount", "Returns the number of CPU ticks.", "", 7),
)

FEATURES_ITEMS = {
    "CV_CPU_NONE": 0,
    "CV_CPU_MMX": 1,
    "CV_CPU_SSE": 2,
    "CV_CPU_SSE2": 3,
    "CV_CPU_SSE3": 4,
    "CV_CPU_SSSE3": 5,
    "CV_CPU_SSE4_1": 6,
    "CV_CPU_SSE4_2": 7,
    "CV_CPU_POPCNT": 8,
    "CV_CPU_FP16": 9,
    "CV_CPU_AVX": 10,
    "CV_CPU_AVX2": 11,
    "CV_CPU_FMA3": 12,
    "CV_CPU_AVX_512F": 13,
    "CV_CPU_AVX_512BW": 14,
    "CV_CPU_AVX_512CD": 15,
    "CV_CPU_AVX_512DQ": 16,
    "CV_CPU_AVX_512ER": 17,
    "CV_CPU_AVX_512IFMA512": 18,
    "CV_CPU_AVX_512IFMA": 18,
    "CV_CPU_AVX_512PF": 19,
    "CV_CPU_AVX_512VBMI": 20,
    "CV_CPU_AVX_512VL": 21,
    "CV_CPU_AVX_512VBMI2": 22,
    "CV_CPU_AVX_512VNNI": 23,
    "CV_CPU_AVX_512BITALG": 24,
    "CV_CPU_AVX_512VPOPCNTDQ": 25,
    "CV_CPU_AVX_5124VNNIW": 26,
    "CV_CPU_AVX_5124FMAPS": 27,
    "CV_CPU_NEON": 100,
    "CV_CPU_VSX": 200,
    "CV_CPU_VSX3": 201,
}


class OCVLsystemNode(OCVLNodeBase):

    n_doc = "OpenCV Utility and System Functions and Macros."

    loc_macros: bpy.props.EnumProperty(items=MACROS_ITEMS, default="getBuildInformation", update=update_node, description="System function.")

    def init(self, context):
        self.width = 700

    def wrapped_process(self):
        pass

    def draw_buttons(self, context, layout):
        self.add_button(layout, 'loc_macros')
        fn = getattr(cv2, self.loc_macros)
        if self.loc_macros == "checkHardwareSupport":
            self._show_check_hardware_support(layout)
            return

        text = str(fn())
        layout.label(text="Function: {}".format(fn))
        for msg in text.split("\n"):
            layout.label(text=msg)

    def _show_check_hardware_support(self, layout):
        for name, index in FEATURES_ITEMS.items():
            layout.label(text="{}: {}".format(name, cv2.checkHardwareSupport(index)))
