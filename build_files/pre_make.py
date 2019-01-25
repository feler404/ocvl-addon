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
BLENDER_BUILD_DIR = os.path.normpath(get_blender_build_path(BLENDER_BUILD_DIR_NAME))
OCVL_ADDON_DIR = "ocvl-addon"
BLENDER_SOURCE_DIR = "blender"
GET_PIP_FILE_NAME = "get-pip.py"
GET_PIP_URL = f"https://bootstrap.pypa.io/{GET_PIP_FILE_NAME}"
OCVL_REQUIREMENTS_PATH = os.path.join(BLENDER_BUILD_DIR, OCVL_ADDON_DIR, "requirements.txt")
WORK_DIR = os.getcwd()


def update_blender(branch='master'):
    """
    Update Blender
    :return:
    """
    os.chdir(os.path.join(BLENDER_BUILD_DIR, BLENDER_SOURCE_DIR))
    cmd(f"git resert --hard")
    cmd(f"git checkout {branch}")
    cmd(f"git pull")
    os.chdir(WORK_DIR)


def update_blender_submodule(branch='master'):
    """
    Update Blender submodules
    :param branch:
    :return:
    """
    os.chdir(os.path.join(BLENDER_BUILD_DIR, BLENDER_SOURCE_DIR))
    cmd(f"git submodule foreach git checkout {branch}")
    cmd(f"git submodule foreach git pull --rebase origin {branch}")
    os.chdir(WORK_DIR)


def update_ocvl_addon(branch='master'):
    """
    Update OCVL ADDON
    :return:
    """
    os.chdir(os.path.join(BLENDER_BUILD_DIR, OCVL_ADDON_DIR))
    cmd(f"git resert --hard")
    cmd(f"git checkout {branch}")
    cmd(f"git pull")
    os.chdir(WORK_DIR)


def build_blender(version="lite"):
    os.chdir(os.path.join(BLENDER_BUILD_DIR, BLENDER_SOURCE_DIR))
    print(os.listdir(os.path.join(BLENDER_BUILD_DIR, BLENDER_SOURCE_DIR)))
    cmd(f"make.bat clean")
    cmd(f"make.bat {version}")
    os.chdir(WORK_DIR)


def get_get_pip_script():
    """
    Get get-pip file from remote server
    :return:
    """
    if not os.path.isfile("{}".format(os.path.join(BLENDER_BUILD_DIR, GET_PIP_FILE_NAME))):
        # ----- GetPIP download
        # cmd(f"cd {BLENDER_BUILD_DIR}")
        cmd(f"curl {GET_PIP_URL} -o {GET_PIP_FILE_NAME}")
        # get_pip_path = os.path.join(os.getcwd(), "get-pip.py")
        # cmd(f"{BLENDER_PYTHON_BIN} {get_pip_path}")


# # ----- Install requirements
# cmd("{} install -r {}".format(BLENDER_PYTHON_PIP_BIN, OCVL_REQUIREMENTS_PATH))
#
# # ----- Replace files
# OCVL_RELEASE_DIR = os.path.join(BLENDER_BUILD_DIR, OCVL_ADDON_DIR, "build_files", "release") + "/"
# BLENDER_RELEASE_DIR = os.path.join(BLENDER_BUILD_DIR, BLENDER_SOURCE_DIR, "release")
# cmd("cp -Rfv {} {}".format(OCVL_RELEASE_DIR, BLENDER_RELEASE_DIR))



try:
    # update_blender(branch="blender2.8")
    # update_blender_submodule()
    build_blender()
finally:
    os.chdir(WORK_DIR)