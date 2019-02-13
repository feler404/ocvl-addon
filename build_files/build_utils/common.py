import os

import subprocess
import sys


def get_blender_build_path(blender_build_dir_name, cwd):
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


def cmd(bash_cmd, accepted_status_code=None, stdout=None):
    accepted_status_code = accepted_status_code or [0]
    stdout = stdout or sys.stdout
    print("-----CMD-----")
    print(bash_cmd)
    process = subprocess.Popen(bash_cmd.split(), stdout=stdout, stderr=sys.stderr)
    out, err = process.communicate()
    if process.returncode not in accepted_status_code:
        raise Exception(f"Status code from command {bash_cmd}: {process.returncode}")
    print("-----SUCCESS----")
    return out, err