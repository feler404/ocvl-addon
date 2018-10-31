#!/usr/bin/env bash
set -x
#
# - blender_build
# -- ocvl-addon
# -- blender
# -- lib
# -- build_darwin
# -- build_darwin_lite
#

# -----  Settings
BLENDER_BUILD_DIR=/Users/dawidaniol/workspace/blender-build
OCVL_ADDON_DIR=ocvl-addon
BLENDER_PYTHON_BIN=/Users/dawidaniol/workspace/blender-build/lib/darwin/python/bin/python3.7m
BLENDER_PYTHON_PIP_BIN=/Users/dawidaniol/workspace/blender-build/lib/darwin/python/bin/pip
GETPIP_URL=https://bootstrap.pypa.io/get-pip.py
OCVL_REQUIREMENTS_PATH=$BLENDER_BUILD_DIR/$OCVL_ADDON_DIR/requirements.txt


# ------ Update OCVL ADDON
cd $BLENDER_BUILD_DIR/$OCVL_ADDON_DIR
#git resert --hard
#git checkout master
#git pull
cd -

if [ ! -f $BLENDER_PYTHON_PIP_BIN ]; then
    # ----- GetPIP download
    curl $GETPIP_URL -o get-pip.py
    $BLENDER_PYTHON_BIN get-pip.py
fi

# ----- Install requirements
$BLENDER_PYTHON_PIP_BIN install -r $OCVL_REQUIREMENTS_PATH

# ----- Replace files
mv $BLENDER_BUILD_DIR/$OCVL_ADDON_DIR/build_files/splash_2x.png $BLENDER_BUILD_DIR/blender/release/datafiles/splash_2x.png
