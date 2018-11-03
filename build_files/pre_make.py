import os
import subprocess
import shutil
#
# - blender_build
# -- ocvl-addon
# -- blender
# -- lib
# -- build_darwin
# -- build_darwin_lite
#


# -----  Settings
BLENDER_BUILD_DIR = "/Users/dawidaniol/workspace/blender-build"
OCVL_ADDON_DIR = "ocvl-addon"
BLENDER_SOURCE_DIR = "blender"
BLENDER_PYTHON_BIN = "/Users/dawidaniol/workspace/blender-build/lib/darwin/python/bin/python3.7m"
BLENDER_PYTHON_PIP_BIN = "/Users/dawidaniol/workspace/blender-build/lib/darwin/python/bin/pip"
GETPIP_URL = "https://bootstrap.pypa.io/get-pip.py"
OCVL_REQUIREMENTS_PATH = os.path.join(BLENDER_BUILD_DIR, OCVL_ADDON_DIR, "requirements.txt")


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

# ------ Update OCVL ADDON
#cd $BLENDER_BUILD_DIR/$OCVL_ADDON_DIR
#git resert --hard
#git checkout master
#git pull
#cd -


if not os.path.isfile(BLENDER_PYTHON_PIP_BIN):
    # ----- GetPIP download
    cmd("curl {} -o get-pip.py".format(GETPIP_URL))
    cmd("{} get-pip.py".format(BLENDER_PYTHON_BIN))


# ----- Install requirements
cmd("{} install -r {}".format(BLENDER_PYTHON_PIP_BIN, OCVL_REQUIREMENTS_PATH))

# ----- Replace files
OCVL_RELEASE_DIR = os.path.join(BLENDER_BUILD_DIR, OCVL_ADDON_DIR, "build_files", "release") + "/"
BLENDER_RELEASE_DIR = os.path.join(BLENDER_BUILD_DIR, BLENDER_SOURCE_DIR, "release")
cmd("cp -Rfv {} {}".format(OCVL_RELEASE_DIR, BLENDER_RELEASE_DIR))
