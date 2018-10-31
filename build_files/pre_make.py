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
#mv $BLENDER_BUILD_DIR/$OCVL_ADDON_DIR/build_files/splash_2x.png $BLENDER_BUILD_DIR/blender/release/datafiles/splash_2x.png


shutil.copy
OCVL_DIR = os.path.join(BLENDER_BUILD_DIR, OCVL_ADDON_DIR)
for path, dirs, files in os.walk(os.path.join(BLENDER_BUILD_DIR, BLENDER_SOURCE_DIR)):
    for file in files:
        src_full_path = os.path.join(path, file)
        last_dir = src_full_path.replace(OCVL_DIR, "")
        dst_full_path = os.path.join(BLENDER_BUILD_DIR, "blender", last_dir)




files = [
    'release/datafiles/blender_icons.svg',  # prawdopodobnie do instalek na mac/linux
    'release/datafiles/splash_2x.png',  # mala wersja splasha
    'release/datafiles/splash_2x.png',  # duza wersja splasha
]