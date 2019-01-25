import os
import subprocess
import shutil
#
# - blender-build
# -- ocvl-addon
# -- blender
# -- lib
# -- build_darwin
# -- build_darwin_lite
#


def get_blender_build_path(blender_build_dir_name):
    cwd = os.getcwd()
    out = True
    head, tail = os.path.split(cwd)
    while out:
        head, tail = os.path.split(head)
        if tail is '':
            raise Exception(f"Can't find '{blender_build_dir_name}' in path")
        if tail == blender_build_dir_name:
            out = False

    return os.path.join(head, blender_build_dir_name)


def cmd(bash_cmd):
    print("-----CMD-----")
    print(bash_cmd)
    process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print("-----OUTPUT----")
    print(output)
    if error:
        print("-----ERROR----")
        print(error)


# -----  Settings
BLENDER_BUILD_DIR_NAME = "blender-build"
BLENDER_BUILD_DIR = get_blender_build_path(BLENDER_BUILD_DIR_NAME)
OCVL_ADDON_DIR = "ocvl-addon"
BLENDER_SOURCE_DIR = "blender"
GETPIP_URL = "https://bootstrap.pypa.io/get-pip.py"
OCVL_REQUIREMENTS_PATH = os.path.join(BLENDER_BUILD_DIR, OCVL_ADDON_DIR, "requirements.txt")



def updaet_ocvl_addon():
    """
    Update OCVL ADDON
    :return:
    """
    cmd(f"cd {$BLENDER_BUILD_DIR}/{OCVL_ADDON_DIR}")
    cmd(f"git resert --hard")
    cmd(f"git checkout master")
    cmd(f"git pull")
    cmd(f"cd -")


# if not os.path.isfile(BLENDER_PYTHON_PIP_BIN):
#     # ----- GetPIP download
#     cmd(f"curl {GETPIP_URL} -o get-pip.py")
#     get_pip_path = os.path.join(os.getcwd(), "get-pip.py")
#     cmd(f"{BLENDER_PYTHON_BIN} {get_pip_path}")


# # ----- Install requirements
# cmd("{} install -r {}".format(BLENDER_PYTHON_PIP_BIN, OCVL_REQUIREMENTS_PATH))
#
# # ----- Replace files
# OCVL_RELEASE_DIR = os.path.join(BLENDER_BUILD_DIR, OCVL_ADDON_DIR, "build_files", "release") + "/"
# BLENDER_RELEASE_DIR = os.path.join(BLENDER_BUILD_DIR, BLENDER_SOURCE_DIR, "release")
# cmd("cp -Rfv {} {}".format(OCVL_RELEASE_DIR, BLENDER_RELEASE_DIR))
