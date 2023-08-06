import os

from uip.constants import constants
from uip.exceptions import customexceptions
from uip.uipproject.uipproject import get_dot_uip_config_file_path
from uip.utils import generic, io, formatting

from .. import UIP_CLI_VERSION, package_dir


def get_global_config_file_dir():
    """
    Based on the OS, it returns the full 
    path of the configuration file directory

    Returns
    -------
    config_dir : str
        Full path of the configuration file directory
    """
    config_dir = None
    home_dir = os.path.expanduser("~")
    os_name = generic.get_os_name()
    if os_name == 'windows':
        config_dir = '%s\\AppData\\Local\\UIP\\config' % home_dir
    elif os_name == 'linux' or os_name == 'darwin':
        config_dir = '%s/.config/uip/config' % home_dir
    else:
        raise customexceptions.PlatformError(208, os_name)
    return config_dir


def get_global_config_file_path():
    """
    Based on the OS, it returns the full path 
    of the configuration file. Note the filename is
    included as part of the path

    Returns
    -------
    str
        Full path of the configuration file
    """
    config_dir = get_global_config_file_dir()
    if config_dir:
        os_name = generic.get_os_name()
        if os_name == 'windows':
            return '%s\\%s' % (config_dir, constants.CONFIG_FILE_NAME)
        elif os_name == 'linux' or os_name == 'darwin':
            return '%s/%s' % (config_dir, constants.CONFIG_FILE_NAME)
        else:
            raise customexceptions.PlatformError(208, os_name)
    else:
        return None


def create_global_config_file():
    global_config_file = get_global_config_file_path()
    if not os.path.exists(global_config_file):
        dest = get_global_config_file_dir()
        if dest:
            io.make_dir(dest)
            config_file_dir = os.path.join(package_dir, constants.CONFIG_FILE_DIR_NAME)
            variables = {'UIP_CLI_VERSION': UIP_CLI_VERSION}
            rendered_config_file = formatting.jinja_render_file(config_file_dir, constants.CONFIG_FILE_NAME, variables)
            io.write_to_file(os.path.join(dest, constants.CONFIG_FILE_NAME), rendered_config_file)
    else:
        #TODO: implement configuration file upgrade logic
        # import linecache
        # current_version = linecache.getline(global_config_file, 6).strip()
        # if current_version != ('# %s' % UIP_CLI_VERSION):
        #     current_config = io.read_yaml(global_config_file)
        #     dest = get_global_config_file_dir()
        #     if dest:
        #         io.make_dir(dest)
        #         config_file_dir = os.path.join(package_dir, constants.CONFIG_FILE_DIR_NAME)
        #         variables = {'UIP_CLI_VERSION': UIP_CLI_VERSION}
        #         rendered_config_file = formatting.jinja_render_file(config_file_dir, constants.CONFIG_FILE_NAME, variables)
        #         io.write_to_file(os.path.join(dest, constants.CONFIG_FILE_NAME), rendered_config_file)
        #         if current_config:
        #             with open(os.path.join(dest, constants.CONFIG_FILE_NAME), 'a') as yml_file:
        #                 import yaml 
        #                 yml_file.write('\n')
        #                 yaml.safe_dump(current_config, yml_file)
        pass


def get_local_config_file_path(relative_to=os.getcwd()):
    return get_dot_uip_config_file_path(relative_to=relative_to)
