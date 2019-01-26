"""
Script to full build and release OpenCV Laboratory on base updated Blender

Structure of directories

* - blender-build
* -- ocvl-addon
* -- blender
* -- lib
* -- build_darwin
* -- build_darwin_lite

"""
import os
import shutil
import sys
import platform
import subprocess


def get_blender_build_path(blender_build_dir_name):
    cwd = os.path.dirname(os.path.realpath(__file__))
    out = True
    head, tail = os.path.split(cwd)
    while out:
        head, tail = os.path.split(head)
        if tail is '':
            raise Exception(f"Can't find '{blender_build_dir_name}' in path")
        if tail == blender_build_dir_name:
            out = False

    cwd = os.path.join(head, blender_build_dir_name)
    print(f"Current work directory: {cwd}")
    return cwd


def cmd(bash_cmd, accepted_status_code=None):
    accepted_status_code = accepted_status_code or [0]
    print("-----CMD-----")
    print(bash_cmd)
    process = subprocess.Popen(bash_cmd.split(), stdout=sys.stdout, stderr=sys.stderr)
    _, _ = process.communicate()
    if process.returncode not in accepted_status_code:
        raise Exception(f"Status code from command {bash_cmd}: {process.returncode}")
    print("-----SUCCESS----")

# -----  Settings
BLENDER_BUILD_DIR_NAME = "blender-build"
WORK_DIR = os.path.normpath(get_blender_build_path(BLENDER_BUILD_DIR_NAME))
OCVL_ADDON_DIR_NAME = "ocvl-addon"
BLENDER_SOURCE_DIR_NAME = "blender"
GET_PIP_FILE_NAME = "get-pip.py"
GET_PIP_URL = f"https://bootstrap.pypa.io/{GET_PIP_FILE_NAME}"
OCVL_REQUIREMENTS_PATH = os.path.join(WORK_DIR, OCVL_ADDON_DIR_NAME, "requirements.txt")
MAKE_COMMAND_MAP = {"Windows": "make.bat", "Linux": "", "Darwin": ""}
MAKE_COMMAND = MAKE_COMMAND_MAP.get(platform.system())

BUILD_VERSION = 'lite'
BUILD_RELEASE_DIRNAME = "build_windows_{}_x64_vc15_Release".format(BUILD_VERSION.capitalize())
BLENDER_PYTHON_BIN = os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, "bin", "Release", "2.80", "python", "bin", "python")
BLENDER_PIP_BIN = os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, "bin", "Release", "2.80", "python", "Scripts", "pip")


def update_blender(branch='master'):
    """
    Update Blender
    :return:
    """
    os.chdir(os.path.join(WORK_DIR, BLENDER_SOURCE_DIR_NAME))
    cmd(f"git reset --hard")
    cmd(f"git checkout {branch}")
    cmd(f"git pull", accepted_status_code=[0, 1])
    os.chdir(WORK_DIR)


def update_blender_submodule(branch='master'):
    """
    Update Blender submodules
    :param branch:
    :return:
    """
    os.chdir(os.path.join(WORK_DIR, BLENDER_SOURCE_DIR_NAME))
    cmd(f"git submodule foreach git checkout {branch}")
    cmd(f"git submodule foreach git pull --rebase origin {branch}")
    os.chdir(WORK_DIR)


def update_ocvl_addon(branch='master'):
    """
    Update OCVL ADDON
    :return:
    """
    os.chdir(os.path.join(WORK_DIR, OCVL_ADDON_DIR_NAME))
    cmd(f"git resert --hard")
    cmd(f"git checkout {branch}")
    cmd(f"git pull")
    os.chdir(WORK_DIR)


def build_blender(build_version=BUILD_VERSION):
    os.chdir(os.path.join(WORK_DIR, BLENDER_SOURCE_DIR_NAME))
    cmd(f"{MAKE_COMMAND} {build_version}")
    os.chdir(WORK_DIR)


def get_get_pip_script():
    """
    Get get-pip file from remote server
    :return:
    """
    os.chdir(WORK_DIR)
    get_pip_filepath = os.path.join(WORK_DIR, GET_PIP_FILE_NAME)
    if not os.path.isfile(f"{get_pip_filepath}"):
        cmd(f"curl {GET_PIP_URL} -o {GET_PIP_FILE_NAME}")

    cmd(f"{BLENDER_PYTHON_BIN} {get_pip_filepath}")
    os.chdir(WORK_DIR)


def install_ocvl_requirements():
    """
    Install requirements.txt in Blender Python
    :return:
    """
    def remove_old_numpy():
        cmd(f"{BLENDER_PIP_BIN} uninstall -y numpy")
        destination_path = os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, "bin", "Release", "2.80", "python", "lib",
                                        "site-packages", "numpy")
        if os.path.exists(destination_path):
            print("Remove old version Numpy")
            shutil.rmtree(destination_path)
    remove_old_numpy()
    cmd(f"{BLENDER_PIP_BIN} install -r {OCVL_REQUIREMENTS_PATH}")
    os.chdir(WORK_DIR)


def copy_ocvl_to_addons():
    """
    Copy(and overwrite) OCVL addon to Blender scripts directory
    :return:
    """
    print("Copy OCVL addon to Blender...")
    source_path = os.path.join(WORK_DIR, OCVL_ADDON_DIR_NAME)
    destination_path = os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, "bin", "Release", "2.80", "scripts", "addons", "ocvl-addon")
    print(f"Copy OCVL addon to Blender. From: {source_path} to {destination_path}...")
    if os.path.exists(destination_path):
        print("Remove old version OCVL addon")
        shutil.rmtree(destination_path)
    shutil.copytree(source_path, destination_path)
    os.chdir(WORK_DIR)
    print("Success!")


try:
    #update_blender(branch="blender2.8")
    #update_blender_submodule()
    #update_ocvl_addon()
    #build_blender()
    get_get_pip_script()
    install_ocvl_requirements()
    copy_ocvl_to_addons()
    pass
finally:
    os.chdir(WORK_DIR)
