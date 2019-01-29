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
import functools
import os
import shutil
import sys
import platform
import subprocess
import os.path
import tarfile


def nsis_installer_build(version_display, build_blender_path, bf_build_dir, rel_dir):

    VERSION = version_display[0:3]
    BF_INSTALLDIR = f"{bf_build_dir}/bin/Release"

    print("="*35)
    bitness = '64'
    bf_installdir = os.path.normpath(os.path.join(build_blender_path, BF_INSTALLDIR))

    doneroot = False
    rootdirconts = []
    datafiles = ''
    deldatafiles = ''
    deldatadirs = ''
    len_bf_installdir = len(bf_installdir)

    for dp, dn, df in os.walk(bf_installdir):
        # install
        if not doneroot:
            for f in df:
                rootdirconts.append(os.path.join(dp, f))
            doneroot = True
        else:
            if len(df) > 0:
                datafiles += "\n" + r'SetOutPath $INSTDIR' + dp[len_bf_installdir:] + "\n\n"

                for f in df:
                    outfile = os.path.join(dp, f)
                    if " " in outfile:
                        print(f"WARNING: filename with space character: {outfile}")
                        continue
                    datafiles += '  File '+outfile + "\n"

        # uninstall
        deldir = dp[len_bf_installdir+1:]

        if len(deldir) > 0:
            deldatadirs = "RMDir $INSTDIR\\" + deldir + "\n" + deldatadirs
            deldatadirs = "RMDir /r $INSTDIR\\" + deldir + "\\__pycache__\n" + deldatadirs

            for f in df:
                deldatafiles += 'Delete \"$INSTDIR\\' + os.path.join(deldir, f) + "\"\n"

    # change to suit install dir
    inst_dir = bf_installdir

    ns = open(os.path.join(rel_dir, "00.sconsblender.nsi"), "r")
    ns_cnt = str(ns.read())
    ns.close()

    # var replacements
    ns_cnt = ns_cnt.replace("[DISTDIR]", os.path.normpath(inst_dir+os.sep))
    ns_cnt = ns_cnt.replace("[VERSION]", version_display)
    ns_cnt = ns_cnt.replace("[SHORTVERSION]", VERSION)
    ns_cnt = ns_cnt.replace("[RELDIR]", os.path.normpath(rel_dir))
    ns_cnt = ns_cnt.replace("[BITNESS]", bitness)

    # do root
    rootlist = []
    for rootitem in rootdirconts:
        rootlist.append("File \"" + rootitem + "\"")
    rootstring = "\n  ".join(rootlist)
    rootstring += "\n\n"
    ns_cnt = ns_cnt.replace("[ROOTDIRCONTS]", rootstring)

    # do delete items
    delrootlist = []
    for rootitem in rootdirconts:
        delrootlist.append("Delete $INSTDIR\\" + rootitem[len_bf_installdir+1:])
    del_root_string = "\n ".join(delrootlist)
    del_root_string += "\n"
    ns_cnt = ns_cnt.replace("[DELROOTDIRCONTS]", del_root_string)

    ns_cnt = ns_cnt.replace("[DODATAFILES]", datafiles)
    ns_cnt = ns_cnt.replace("[DELDATAFILES]", deldatafiles)
    ns_cnt = ns_cnt.replace("[DELDATADIRS]", deldatadirs)

    tmpnsi = os.path.normpath(build_blender_path + os.sep + bf_build_dir + os.sep + "00.blender_tmp.nsi")
    print(f"Temp nsi file: {tmpnsi}")
    new_nsis = open(tmpnsi, 'w')
    new_nsis.write(ns_cnt)
    new_nsis.close()
    print("NSIS Installer script created")


    print("Launching 'makensis'")

    cmdline = "makensis " + "\""+tmpnsi+"\""

    startupinfo = subprocess.STARTUPINFO()
    #  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    proc = subprocess.Popen(
        cmdline,
        stdin=subprocess.PIPE,
        stdout=sys.stdout,
        stderr=sys.stderr,
        startupinfo=startupinfo,
        shell=True
    )
    data, err = proc.communicate()
    rv = proc.wait()

    if rv != 0:
        print(f"Data: {data}")
        print(f"Errors: {err}")

    print("Compilation Success!")
    print(f"Output file in {bf_installdir}")
    return rv


def make_tar_gz_form_release():
    """
    Make tar.gz archive from release fiels
    :return:
    """
    source = os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, BIN_RELEASE)
    destination = os.path.join(WORK_DIR, f"OCVL-{OCVL_VERSION}-linux.tar.gz")
    with tarfile.open(destination, "w:gz") as tar:
        tar.add(source, arcname=os.path.basename(source))
    print(f"Success. Artifact available on: {destination}")


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
PLATFORM = platform.system()
OCVL_VERSION = "1.2.0.0"
BLENDER_BUILD_DIR_NAME = "blender-build"
WORK_DIR = os.path.normpath(get_blender_build_path(BLENDER_BUILD_DIR_NAME))
OCVL_ADDON_DIR_NAME = "ocvl-addon"
BLENDER_SOURCE_DIR_NAME = "blender"
GET_PIP_FILE_NAME = "get-pip.py"
GET_PIP_URL = f"https://bootstrap.pypa.io/{GET_PIP_FILE_NAME}"
OCVL_REQUIREMENTS_PATH = os.path.join(WORK_DIR, OCVL_ADDON_DIR_NAME, "requirements.txt")
MAKE_COMMAND_MAP = {"Windows": "make.bat", "Linux": "make", "Darwin": "make"}
MAKE_COMMAND = MAKE_COMMAND_MAP[PLATFORM]

BUILD_VERSION = 'lite'
BUILD_RELEASE_DIRNAME_TEMPLATE_MAP = {
    "Windows": "build_windows_{}_x64_vc15_Release".format(BUILD_VERSION.capitalize()),
    "Linux": f"build_linux_{BUILD_VERSION}",
    "Darwin": f"build_darwin_{BUILD_VERSION}"}
BUILD_RELEASE_DIRNAME = BUILD_RELEASE_DIRNAME_TEMPLATE_MAP[PLATFORM]

BIN_RELEASE_MAP = {
    "Windows": os.path.join("bin", "Release"),
    "Linux": "bin",
    "Darwin": os.path.join("bin", "blender.app", "Contents", "Resources"),
}
BIN_RELEASE = BIN_RELEASE_MAP[PLATFORM]
PYTHON_PACKAGES = "site-packages" if PLATFORM is 'Windows' else os.path.join("python3.7", "dist-packages")
BLENDER_PYTHON_BIN_MAP = {
    "Windows": os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, BIN_RELEASE, "2.80", "python", "bin", "python"),
    "Linux": os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, BIN_RELEASE, "2.80", "python", "bin", "python3.7m"),
    "Darwin": os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, BIN_RELEASE, "2.80", "python", "bin", "python3.7m")
}
BLENDER_PYTHON_BIN = BLENDER_PYTHON_BIN_MAP[PLATFORM]

BLENDER_PIP_BIN_MAP = {
    "Windows": os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, BIN_RELEASE, "2.80", "python", "Scripts", "pip"),
    "Linux": os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, BIN_RELEASE, "2.80", "python", "local", "bin", "pip"),
    "Darwin": os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, BIN_RELEASE, "2.80", "python", "bin", "pip"),
}
BLENDER_PIP_BIN = BLENDER_PIP_BIN_MAP[PLATFORM]
PREPARE_ARTIFACT_FN_MAP = {
    "Windows": functools.partial(
        nsis_installer_build,
        version_display=OCVL_VERSION,
        build_blender_path=WORK_DIR,
        bf_build_dir=BUILD_RELEASE_DIRNAME,
        rel_dir=os.path.join(WORK_DIR, OCVL_ADDON_DIR_NAME, "build_files", "release", "windows")
    ),
    "Linux": make_tar_gz_form_release,
    "Darwin": lambda *args: print(args),
}

PREPARE_ARTIFACT_FN = PREPARE_ARTIFACT_FN_MAP[PLATFORM]

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
        destination_path = os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, BIN_RELEASE, "2.80", "python", "lib",
                                        PYTHON_PACKAGES, "numpy")
        if os.path.exists(destination_path):
            print(f"Remove old version Numpy from: {destination_path}")
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
    destination_path = os.path.join(WORK_DIR, BUILD_RELEASE_DIRNAME, BIN_RELEASE, "2.80", "scripts", "addons", "ocvl-addon")
    print(f"Copy OCVL addon to Blender. From: {source_path} to {destination_path}...")
    if os.path.exists(destination_path):
        print("Remove old version OCVL addon")
        shutil.rmtree(destination_path)
    shutil.copytree(source_path, destination_path)
    os.chdir(WORK_DIR)
    print("Success!")


try:
    #update_blender()
    #update_blender_submodule()
    #update_ocvl_addon()
    #build_blender()
    #get_get_pip_script()
    install_ocvl_requirements()
    copy_ocvl_to_addons()
    PREPARE_ARTIFACT_FN()

    pass
finally:
    os.chdir(WORK_DIR)
