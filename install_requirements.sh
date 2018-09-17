#!/usr/bin/env bash
# EDIT THIS --------------
BLENDER_PYTHON_PATH="/Applications/Blender/blender.app/Contents/Resources/2.79/python/bin"
PTYHON_BIN="python3.5m"
# EDIT THIS ---------------

PYTHON_PIP_PATH=${BLENDER_PYTHON_PATH}/python/bin/pip
BLENDER_PYTHON_PATH_BIN=${BLENDER_PYTHON_PATH}/${PTYHON_BIN}
SOURCE=$(dirname "$BASH_SOURCE[0]")
GETPIP_URL="https://bootstrap.pypa.io/get-pip.py"
GETPIP_FILE_NAME="get-pip.py"

curl $GETPIP_URL -o ${GETPIP_FILE_NAME}

$BLENDER_PYTHON_PATH_BIN ./${GETPIP_FILE_NAME}
$BLENDER_PYTHON_PATH/pip install --upgrade pip
$BLENDER_PYTHON_PATH/pip install -r ${SOURCE}/requirements.txt