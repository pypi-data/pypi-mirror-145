# cliapis errors (1-100)
cliapis_errors = {
    1: 'auth tuple cannot be None',
    2: 'params dictionary cannot be None',
    3: 'response object cannot be None',
    4: 'Universal Template name must be specified',
    5: 'url cannot be empty',
    6: '"{0}" command type not found',
    7: 'url endpoint for "%s" not found',
    8: '"{0}" not found',
    9: 'There are no existing instances of "{0}" task'
}

# cliconfig errors (101-200)
cliconfig_errors = {
    101: '"{0}" is not a JSON file',
    102: '"{0}" is not a PNG file',
    103: '"{0}" is not a ZIP file'
}

# config errors (201-300)
config_errors = {
    201: '"{0}" must be specified',
    202: 'Universal Template name must be specified',
    203: '"{0}" option cannot be None',
    204: '"{0}" configuration file not found',
    205: 'Universal Extension task name must be specified',
    206: '"{0}" is not a valid integer value',
    207: 'value must be a positive integer',
    208: '"{0}" is not a supported platform. Only Windows, Linux, and MacOS are supported'
}

# uipproject errors (301-400)
uipproject_errors = {
    301: '"{0}" is not a valid JSON or YAML file',
    302: '"{0}" is incorrectly formatted',
    303: '{0} folder already exists in "{1}"',
    304: 'error building extension',
    305: 'error building full package',
    306: 'template.json is corrupted. {0}',
    307: '"{0}" already contains an Extension template',
    308: '"{0}" does not contain a valid Extension template',
    309: '"{0}" is not a valid Extension template directory',
    310: 'No zip files were found in "{0}"',
    311: '"{0}" is not a valid Extension template',
    312: 'template.json is corrupted. The "name" field must be non-empty',
    313: '"{0}" not found'
}

# utils errors (401-500)
utils_errors = {
    401: '"{0}" is not a valid JSON string'
}

# parsecli errors (501-600)
parsecli_errors = {
    501: '"{0}" is not a valid folder name',
    502: '"{0}" is not a valid Extension template',
    503: '"{0}" is not a valid Universal Extension task',
    504: '"{0}" is not a valid task instance number'
}

error_messages = {}
error_messages.update(cliapis_errors)
error_messages.update(cliconfig_errors)
error_messages.update(config_errors)
error_messages.update(uipproject_errors)
error_messages.update(utils_errors)
error_messages.update(parsecli_errors)