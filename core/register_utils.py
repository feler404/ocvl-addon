import sys
from importlib import reload
import bpy


def try_register(klass):
    try:
        bpy.utils.register_class(klass)
    except Exception as e:
        pass


def try_unregister(klass):

    try:
        bpy.utils.unregister_class(klass)
    except Exception as e:
        print (1111, e)


def ocvl_register(klass):
    print("Register: {}".format(klass))
    try_register(klass)


def ocvl_unregister(klass):
    try_unregister(klass)


def reload_ocvl_modules():

    for module_name in sys.modules.keys():
        if "ocvl" in module_name:
            reload(sys.modules[module_name])

