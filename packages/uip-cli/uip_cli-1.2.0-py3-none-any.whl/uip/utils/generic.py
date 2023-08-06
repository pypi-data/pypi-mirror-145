import copy
import os
import platform
import subprocess
import sys
import uuid


def generate_uuid(remove_dashes=True):
    random_uuid = str(uuid.uuid4())
    return random_uuid.replace('-', '') if remove_dashes else random_uuid


def get_os_name():
    return platform.system().lower()


def deep_copy_dict(original_dict):
    return copy.deepcopy(original_dict)


def pip_install(path_to_requirements_txt, install_to):
    if os.path.exists(path_to_requirements_txt) and os.path.exists(install_to):
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-r', path_to_requirements_txt, '-t', install_to])
