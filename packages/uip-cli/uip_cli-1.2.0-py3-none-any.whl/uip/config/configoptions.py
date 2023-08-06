from uip.utils import generic
import os

login_options = {
    'userid': {'short_arg': '-u', 'long_arg': '--userid', 'env_var': 'UIP_USERID', 'config_arg': 'userid',
               'default': None},
    'password': {'short_arg': '-w', 'long_arg': '--password', 'env_var': 'UIP_PASSWORD', 'config_arg': None,
                 'default': None},
    'url': {'short_arg': '-i', 'long_arg': '--url', 'env_var': 'UIP_URL', 'config_arg': 'url', 'default': None},
}

config_options = {
    'shared': {
        # options that are shared across the various commands
    },
    'init': {
        'extension_template': {'short_arg': '-t', 'long_arg': '--extension-template', 'env_var': None,
                               'config_arg': None, 'default': None},
        'variables': {'short_arg': '-e', 'long_arg': '--variables', 'env_var': 'UIP_TEMPLATE_VARIABLES',
                      'config_arg': 'variables', 'default': None},
        'dir': {'default': os.getcwd()}
    },
    'build': {
        'all': {'short_arg': '-a', 'long_arg': '--all', 'env_var': 'UIP_BUILD_ALL', 'config_arg': 'build-all',
                'default': False}
    },
    'upload': {
        'all': {'short_arg': '-a', 'long_arg': '--all', 'env_var': 'UIP_UPLOAD_ALL', 'config_arg': 'upload-all',
                'default': False},
    },
    'push': {
        'all': {'short_arg': '-a', 'long_arg': '--all', 'env_var': 'UIP_PUSH_ALL', 'config_arg': 'push-all',
                'default': False},
    },
    'pull': {
    },
    'download': {
        'template_name': {'short_arg': '-n', 'long_arg': '--template-name', 'env_var': 'UIP_TEMPLATE_NAME',
                          'config_arg': 'template-name', 'default': None},
    },
    'task_launch': {
        'task_name': {'default': None},
        'no_wait': {'short_arg': '-N', 'long_arg': '--no-wait', 'env_var': 'UIP_NO_WAIT', 'config_arg': 'no-wait',
                    'default': False},
    },
    'task_status': {
        'task_name': {'default': None},
        'num_instances': {'short_arg': '-n', 'long_arg': '--num-instances', 'env_var': 'UIP_NUM_INSTANCES', 'config_arg': 'num-instances',
                    'default': 1},
    },
    'task_output': {
        'task_name': {'default': None},
        'instance_number': {'short_arg': '-s', 'long_arg': '--instance-number', 'env_var': 'UIP_INSTANCE_NUMBER', 'config_arg': 'instance-number',
                    'default': 'most_recent_task_instance'},
    }
}

for config_option in ['shared', 'upload', 'push', 'pull', 'download', 'task_launch', 'task_status', 'task_output']:
    config_options[config_option].update(login_options)


def get_config_options_dict():
    return generic.deep_copy_dict(config_options)


def get_value(option, attribute):
    option_dest = option.split('.')

    value = get_config_options_dict()
    for dest in option_dest:
        value = value.get(dest, {})

    return value.get(attribute, None)


def get_short_arg(option):
    return get_value(option, 'short_arg')


def get_long_arg(option):
    return get_value(option, 'long_arg')


def get_env_var_name(option):
    return get_value(option, 'env_var')


def get_config_arg(option):
    return get_value(option, 'config_arg')


def get_default_value(option):
    return get_value(option, 'default')
