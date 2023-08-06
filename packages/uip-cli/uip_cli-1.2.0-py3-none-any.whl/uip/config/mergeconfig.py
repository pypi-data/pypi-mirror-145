import argparse
import os

from uip.exceptions import customexceptions
from uip.utils import io, generic

from .config import get_global_config_file_path, get_local_config_file_path
from .configoptions import get_config_options_dict
from .verifyconfig import verify_command, is_value_empty_string


def get_env_var_value(option):
    value = os.environ.get(option, None)
    quotes_stripped = True
    while value and quotes_stripped:
        quotes_stripped = False
        for quote in ['"', "'"]:
            if value.startswith(quote) and value.endswith(quote):
                value = value.strip(quote)
                quotes_stripped = True
    if is_value_empty_string(value):
        value = None
    return value


def get_config_option_value(config_file_path, option):
    if config_file_path:
        if not os.path.exists(config_file_path):
            raise customexceptions.FileNotFoundError(204, config_file_path)

        config_file = io.read_yaml(config_file_path)

        if config_file and option in config_file:
            value = config_file[option]
            if is_value_empty_string(value):
                value = None
            return value
        else:
            return None
    else:
        return None


def get_merged_config_helper(command, cli_args):
    # cli_args > env vars > local config file (.uip/config/config.yml) > global config file > default values
    cli_args_dict = vars(cli_args)

    command_path = command.split('.')
    options = get_config_options_dict()
    for dest in command_path:
        options = options.get(dest, {})

    merged_config = {}
    for option in options:
        option_config = options.get(option, {})
        if option_config:
            merged_config[option] = None

            if cli_args_dict.get(option, None) is not None:
                value = cli_args_dict[option]
                merged_config[option] = value

            if (merged_config[option] is None) and option_config.get('env_var', '') and \
                    get_env_var_value(option_config['env_var']):
                env_var_value = get_env_var_value(option_config['env_var'])
                if env_var_value:
                    merged_config[option] = env_var_value

            config_arg = option_config.get('config_arg', None)

            if merged_config[option] is None:
                # get value from config file in .uip/config
                config_file_path = get_local_config_file_path()
                merged_config[option] = get_config_option_value(config_file_path, config_arg)

            if merged_config[option] is None:
                # get value from default global config file
                config_file_path = get_global_config_file_path()
                merged_config[option] = get_config_option_value(config_file_path, config_arg)

            if merged_config[option] is None:
                # if default config file didn't contain the value, then use default value
                merged_config[option] = option_config.get('default', None)

    # get the 'global' options as well
    if command == 'global':
        return merged_config
    else:
        global_options_config = get_merged_config_helper('global', cli_args)
        merged_config.update(global_options_config)

        # verify the merged_config for the given 'command'
        verify_command(command, merged_config)

        return merged_config


def get_merged_config(command, cli_args):
    merged_config = get_merged_config_helper(command, cli_args)
    mc = generic.deep_copy_dict(vars(cli_args))
    mc.update(merged_config)
    return argparse.Namespace(**mc)
