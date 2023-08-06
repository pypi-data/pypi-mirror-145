import os
import argparse

# cliapis
UNIVERSAL_TEMPLATE_URL_ENDPOINT = 'resources/universaltemplate'
TASK_URL_ENDPOINT = 'resources/task'
TASK_INSTANCE_URL_ENDPOINT = 'resources/taskinstance'

# cliconfig
ADJUSTED_WRAP_LIMIT = '82'

# uipproject
CONFIG_FILE_NAME = 'uip.yml'
CONFIG_FILE_DIR_NAME = 'config'
DOT_UIP_FOLDER_NAME = '.uip'
VALID_EXTENSION_TEMPLATE_FILES = ['src/extension.py', 'src/extension.yml', 'src/templates/template.json', 'setup.py',
                                  'setup.cfg']
VALID_EXTENSION_TEMPLATE_FILES_WITHOUT_SETUP = ['src/extension.py', 'src/extension.yml', 'src/templates/template.json']
SETUP_SCRIPTS_RESOURCES = ['setupscripts/setup.cfg', 'setupscripts/setup.py']
VARIABLES_OPTION_VALUE_DELIMETER = '='
VARIABLES_FILE_PREFIX = '@'
VARIABLES_JSON_STRING_PREFIX = '{'
VARIABLES_JSON_STRING_SUFFIX = '}'
DIST_DIR_NAME = 'dist'
EXTENSION_BUILD_DIR = os.path.join(DIST_DIR_NAME, 'extension_build')
PACKAGE_BUILD_DIR = os.path.join(DIST_DIR_NAME, 'package_build')
PACKAGE_DOWNLOAD_DIR = os.path.join(DIST_DIR_NAME, 'package_download')
TEMP_SAVE_DIR_NAME = 'tmp'
UNIVERSAL_TEMPLATE_DIST_NAME = '%s_universal_template.zip'

# uiptemplates
UUID_INTERNAL_VARIABLES = 'uuid_variables'
TEMPLATE_CONFIG_YAML = 'template_config.yml'
RESOURCES_DIR = os.path.join('uiptemplates', 'resources')

# parsecli
_TASK_STATUSES = {
    'success': 'Success',
    'finished': 'Finished',
    'failed': 'Failed',
    'cancelled': 'Cancelled',
    'start_failure': 'Start Failure',
    'undeliverable': 'Undeliverable',
    'in_doubt': 'In Doubt',
    'skipped': 'Skipped'
}
TASK_STATUSES = argparse.Namespace(**_TASK_STATUSES)