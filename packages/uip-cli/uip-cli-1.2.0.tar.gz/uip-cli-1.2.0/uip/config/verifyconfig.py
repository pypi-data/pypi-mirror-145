import os
import sys

from uip.constants import constants
from uip.exceptions import customexceptions
from uip.uipproject import uipproject
from uip.utils import io, formatting
from .configoptions import get_default_value


def is_value_empty_string(value):
    return type(value) == str and len(value.strip()) == 0


def verify_dir_name(dir):
    if dir is None or is_value_empty_string(dir):
        raise customexceptions.InvalidFolderError(501, dir)


def parse_variables(variables):
    if variables is None or (type(variables) == list and len(variables) == 0):
        return None

    if type(variables) == str:
        variables = [variables]

    parsed_variables = {}
    if len(variables) == 1:
        variables = variables[0]
        equals_index = variables.find(constants.VARIABLES_OPTION_VALUE_DELIMETER)
        starts_ends_with_braces = variables.startswith(constants.VARIABLES_JSON_STRING_PREFIX) and variables.endswith(constants.VARIABLES_JSON_STRING_SUFFIX)
        if equals_index != -1 and starts_ends_with_braces is False:
            option = variables[:equals_index].strip()
            value = variables[equals_index + 1:].strip()
            if len(option) == 0 or len(value) == 0:
                raise customexceptions.InvalidValueError(302, variables)
            parsed_variables = {option: value}
        elif variables.startswith(constants.VARIABLES_FILE_PREFIX):
            variables_file = variables[1:]
            if not os.path.exists(variables_file):
                raise customexceptions.FileNotFoundError(313, variables_file)

            try:
                parsed_variables = io.read_json(variables_file)
                assert type(parsed_variables) == dict
            except Exception as e:
                try:
                    parsed_variables = io.read_yaml(variables_file)
                    assert type(parsed_variables) == dict
                except Exception as e:
                    raise customexceptions.CorruptedFileError(301, variables_file)
        else:
            parsed_variables = formatting.parse_json_string(variables)
            if type(parsed_variables) != dict:
                raise customexceptions.InvalidValueError(302, parsed_variables)
    else:
        for variable in variables:
            equals_index = variable.find(constants.VARIABLES_OPTION_VALUE_DELIMETER)
            if equals_index != -1:
                option = variable[:equals_index].strip()
                value = variable[equals_index + 1:].strip()
                if len(option) == 0 or len(value) == 0:
                    raise customexceptions.InvalidValueError(302, variable)
                parsed_variables[option] = value
            else:
                raise customexceptions.InvalidValueError(302, variable)

    return parsed_variables


def verify_bool(option, value):
    if value is None:
        raise customexceptions.InvalidValueError(203, option)
    elif value == True:
        return True
    elif type(value) == str:
        value = value.strip().lower()
        if value in ['yes', 'true']:
            return True
        else:
            return False
    else:
        return False


def verify_login_options(merged_config):
    for option in ['userid', 'password', 'url']:
        value = merged_config.get(option, None)
        if value is None or is_value_empty_string(value):
            raise customexceptions.MissingValueError(201, option)


def verify_template_name(merged_config):
    template_name = merged_config.get('template_name', None)
    if is_value_empty_string(template_name):
        raise customexceptions.MissingValueError(202)


def verify_task_name(merged_config):
    task_name = merged_config.get('task_name', None)
    if is_value_empty_string(task_name) or task_name is None:
        raise customexceptions.MissingValueError(205)


def verify_init(merged_config):
    variables = merged_config['variables']
    merged_config['variables'] = parse_variables(variables)
    verify_dir_name(merged_config['dir'])


def verify_build(merged_config):
    build_all = merged_config.get('all', None)
    merged_config['all'] = verify_bool('all', build_all)


def verify_upload(merged_config):
    verify_login_options(merged_config)
    upload_all = merged_config.get('all', None)
    merged_config['all'] = verify_bool('all', upload_all)


def verify_push(merged_config):
    verify_login_options(merged_config)
    push_all = merged_config.get('all', None)
    merged_config['all'] = verify_bool('all', push_all)


def verify_pull(merged_config):
    verify_login_options(merged_config)


def verify_download(merged_config):
    verify_login_options(merged_config)
    verify_template_name(merged_config)


def verify_task_launch(merged_config):
    verify_login_options(merged_config)
    verify_task_name(merged_config)
    no_wait = merged_config.get('no_wait', None)
    merged_config['no_wait'] = verify_bool('no_wait', no_wait)


def verify_task_status(merged_config):
    verify_login_options(merged_config)
    verify_task_name(merged_config)
    try:
        merged_config['num_instances'] = int(merged_config['num_instances'])
    except ValueError as ve:
        raise customexceptions.InvalidValueError(206, merged_config['num_instances'])


def verify_task_output(merged_config):
    verify_login_options(merged_config)
    verify_task_name(merged_config)
    try:
        if merged_config['instance_number'] == get_default_value('task_output.instance_number'):
            merged_config['instance_number'] = None 
        else:
            merged_config['instance_number'] = int(merged_config['instance_number'])
    except ValueError as ve:
        raise customexceptions.InvalidValueError(206, merged_config['instance_number'])

    if type(merged_config['instance_number']) == int and merged_config['instance_number'] <= 0:
        raise customexceptions.InvalidValueError(207)


def verify_command(command, merged_config):
    function_name = 'verify_%s' % command.replace('.', '_')
    func = getattr(sys.modules[__name__], function_name, None)
    if func is not None:
        func(merged_config)
