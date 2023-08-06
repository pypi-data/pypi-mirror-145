import os
import zipfile

from jinja2 import Environment, FileSystemLoader
from setuptools import sandbox
from uip.constants import constants
from uip.exceptions import customexceptions
from uip.uiptemplates import template
from uip.utils import formatting, generic, io

from .. import package_dir, UIP_CLI_VERSION


def is_valid_extension_template_dir(dir, require_setup_files=True):
    if not os.path.exists(dir):
        return False

    if require_setup_files:
        valid_extension_template_files = constants.VALID_EXTENSION_TEMPLATE_FILES
    else:
        valid_extension_template_files = constants.VALID_EXTENSION_TEMPLATE_FILES_WITHOUT_SETUP

    for f in valid_extension_template_files:
        if not os.path.exists(os.path.join(dir, f)):
            return False

    return True


def is_valid_dot_uip_dir(dir):
    config_file_path = os.path.join(dir, constants.DOT_UIP_FOLDER_NAME, constants.CONFIG_FILE_DIR_NAME,
                                    constants.CONFIG_FILE_NAME)
    return os.path.exists(config_file_path)


def is_valid_dot_uip_and_extension_template_dir(dir):
    return is_valid_extension_template_dir(dir) and is_valid_dot_uip_dir(dir)


def create_dot_uip_dir(dir, overwrite=False):
    if overwrite or not is_valid_dot_uip_dir(dir):
        dst_config_file_dir = os.path.join(dir, constants.DOT_UIP_FOLDER_NAME, constants.CONFIG_FILE_DIR_NAME)
        io.make_dir(dst_config_file_dir)

        config_file_dir = os.path.join(package_dir, constants.CONFIG_FILE_DIR_NAME)
        variables = {'UIP_CLI_VERSION': UIP_CLI_VERSION}
        rendered_config_file = formatting.jinja_render_file(config_file_dir, constants.CONFIG_FILE_NAME, variables)
        io.write_to_file(os.path.join(dst_config_file_dir, constants.CONFIG_FILE_NAME), rendered_config_file)


def handle_internal_variables(internal_variables):
    parsed_internal_variables = {}
    for variable in internal_variables:
        variable_type = list(variable.keys())[0]
        if variable_type == constants.UUID_INTERNAL_VARIABLES:
            uuid_variables = variable.get(variable_type)
            for uuid_variable in uuid_variables:
                parsed_internal_variables[uuid_variable] = generic.generate_uuid()
    return parsed_internal_variables


def initialize_uip(starter_template_name, variables, dir):
    if starter_template_name is None:
        # attempt to initialize an empty repository
        if is_valid_extension_template_dir(dir, require_setup_files=False):
            if not is_valid_dot_uip_dir(dir):
                create_dot_uip_dir(dir)
                for setup_file in constants.SETUP_SCRIPTS_RESOURCES:
                    setup_file_name = os.path.basename(setup_file)
                    if not os.path.exists(os.path.join(dir, setup_file_name)):
                        template.copy_resources(constants.SETUP_SCRIPTS_RESOURCES, dir)
                        break
                return 'Successfully created %s folder in "%s"' % (constants.DOT_UIP_FOLDER_NAME, dir)
            else:
                raise customexceptions.InitError(303, constants.DOT_UIP_FOLDER_NAME, dir)
        else:
            raise customexceptions.InvalidFolderError(308, dir)
    else:
        extension_template = template.get_extension_templates([starter_template_name])
        if not extension_template:
            raise customexceptions.InvalidValueError(311, starter_template_name)

        if is_valid_dot_uip_and_extension_template_dir(dir):
            raise customexceptions.InitError(307, dir)

        user_defined_variables = variables

        template_path = extension_template[0].get('template_path')
        template_details = template.get_extension_template_details(template_path)
        files_to_template = template_details.get('files_to_template')
        variable_dict = {}
        for variable in template_details.get('user_defined_variables'):
            variable_name = list(variable.keys())[0]
            variable_default = variable[variable_name]['default']
            variable_dict[variable_name] = variable_default

        if user_defined_variables:
            variable_dict.update(user_defined_variables)

        internal_variables = template_details.get('internal_variables', None)
        parsed_internal_variables = handle_internal_variables(internal_variables)
        if parsed_internal_variables:
            variable_dict.update(parsed_internal_variables)

        create_dot_uip_dir(dir, overwrite=True)

        if is_valid_dot_uip_dir(dir):
            template.copy_template(template_path, dir)

            resources_to_copy = template_details.get('resources_to_include', None)
            template.copy_resources(resources_to_copy, dir)

            env = Environment(loader=FileSystemLoader(template_path),
                    keep_trailing_newline=True)
            for file_to_template in files_to_template:
                curr_template = env.get_template(file_to_template)
                rendered_template = curr_template.render(variable_dict)
                io.write_to_file(os.path.join(dir, file_to_template), rendered_template)

            return 'Successfully initialized "%s" template in "%s"' % (starter_template_name, dir)


def get_built_extension_zip_path():
    dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dir):
        search_dir = os.path.join(dir, constants.EXTENSION_BUILD_DIR)
        zip_files = io.get_files_of_specific_type(search_dir, '*.zip')

        if zip_files is None or len(zip_files) == 0:
            raise customexceptions.InvalidFolderError(310, search_dir)

        if len(zip_files) > 1:
            choice = io.read_user_choice('Multiple zip files were found. Please select the one you wish to upload: ',
                                         zip_files)
            return choice
        elif len(zip_files) == 1:
            return zip_files[0]
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def get_built_full_package_zip_path():
    dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dir):
        search_dir = os.path.join(dir, constants.PACKAGE_BUILD_DIR)
        zip_files = io.get_files_of_specific_type(search_dir, '*.zip')

        if zip_files is None or len(zip_files) == 0:
            raise customexceptions.InvalidFolderError(310, search_dir)

        if len(zip_files) > 1:
            choice = io.read_user_choice('Multiple zip files were found. Please select the one you wish to upload: ',
                                         zip_files)
            return choice
        elif len(zip_files) == 1:
            return zip_files[0]
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def get_temporary_save_dir():
    dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dir):
        return os.path.join(dir, constants.DOT_UIP_FOLDER_NAME, constants.TEMP_SAVE_DIR_NAME)
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def get_pull_command_save_dir():
    return get_temporary_save_dir()


def get_download_command_save_dir():
    dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dir):
        return os.path.join(dir, constants.PACKAGE_DOWNLOAD_DIR)
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def move_template_json_icon(move_from):
    if os.path.exists(move_from):
        dot_uip_dir = os.getcwd()
        if is_valid_dot_uip_and_extension_template_dir(dot_uip_dir):
            new_template_json = os.path.join(move_from, 'template.json')
            new_template_icon = os.path.join(move_from, 'template_icon.png')

            move_to = os.path.join(dot_uip_dir, 'src', 'templates')
            curr_template_json = os.path.join(move_to, 'template.json')
            curr_template_icon = os.path.join(move_to, 'template_icon.png')

            changes = {
                'updated_files': [],
                'new_files': [],
                'unchanged_files': []
            }

            for curr_file, new_file in [(curr_template_json, new_template_json),
                                        (curr_template_icon, new_template_icon)]:
                curr_file_md5 = io.get_md5_of_file(curr_file)
                new_file_md5 = io.get_md5_of_file(new_file)

                if curr_file_md5 is None:
                    if new_file_md5:
                        # current file does not exist but new file does
                        changes['new_files'].append(formatting.get_filename_from_path(new_file))
                        io.copy_file(new_file, move_to)
                else:
                    if new_file_md5:
                        if curr_file_md5 == new_file_md5:
                            # current and new file exists, and they are the same
                            changes['unchanged_files'].append(formatting.get_filename_from_path(curr_file))
                        else:
                            # new file differs from current file
                            changes['updated_files'].append(formatting.get_filename_from_path(curr_file))
                            io.copy_file(new_file, move_to)

            io.remove_dir(move_from)
            return changes
        else:
            raise customexceptions.InvalidFolderError(309, dot_uip_dir)


def move_full_package(full_package_path):
    if os.path.exists(full_package_path):
        dot_uip_dir = os.getcwd()
        if is_valid_dot_uip_and_extension_template_dir(dot_uip_dir):
            new_full_package = full_package_path

            move_to = get_download_command_save_dir()

            io.make_dir(move_to)

            existing_zip_files = io.get_files_of_specific_type(move_to, '*.zip')
            curr_full_package = None
            new_full_package_name = formatting.get_filename_from_path(new_full_package)
            for existing_zip_file in existing_zip_files:
                if new_full_package_name == formatting.get_filename_from_path(existing_zip_file):
                    curr_full_package = existing_zip_file
                    break

            changes = {
                'updated_file': '',
                'new_file': '',
                'unchanged_file': ''
            }

            for curr_file, new_file in [(curr_full_package, new_full_package)]:
                curr_file_md5 = io.get_md5_of_zipfile(curr_file)
                new_file_md5 = io.get_md5_of_zipfile(new_file)

                if curr_file_md5 is None:
                    if new_file_md5:
                        # current file does not exist but new file does
                        io.copy_file(new_file, move_to)
                        copied_file_path = io.get_most_recent_file(move_to, '*.zip')
                        changes['new_file'] = formatting.get_relative_path(copied_file_path)
                else:
                    if new_file_md5:
                        if curr_file_md5 == new_file_md5:
                            # current and new file exists, and they are the same
                            changes['unchanged_file'] = formatting.get_relative_path(curr_file)
                        else:
                            # new file differs from current file
                            changes['updated_file'] = formatting.get_relative_path(curr_file)
                            io.copy_file(new_file, move_to)

            io.remove_dir(formatting.get_dir_name(full_package_path))
            return changes
        else:
            raise customexceptions.InvalidFolderError(309, dot_uip_dir)


def get_template_json_property(property):
    dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dir):
        template_json_path = os.path.join(dir, 'src', 'templates', 'template.json')
        try:
            template_json = io.read_json(template_json_path)
            return template_json.get(property, None)
        except ValueError as e:
            raise customexceptions.CorruptedFileError(306, str(e))
    else:
        return None


def get_template_name_from_template_json():
    template_name = get_template_json_property('name')
    if template_name:
        return template_name
    else:
        raise customexceptions.CorruptedFileError(312)


def build_extension(build_dir='extension_build', zip_filename=''):
    dot_uip_dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dot_uip_dir):

        requirements_txt_path = os.path.join(dot_uip_dir, 'requirements.txt')
        if os.path.exists(requirements_txt_path):
            threepp_path = os.path.join(dot_uip_dir, '3pp')
            io.make_dir(threepp_path)

            generic.pip_install(requirements_txt_path, threepp_path)

        try:
            sandbox.run_setup('setup.py', ['clean', 'bdist_egg'])
        except SystemExit:
            pass
        
        print(('=' * 88))
        most_recent_file = io.get_most_recent_file(os.path.join(dot_uip_dir, 'dist'), filetype='*.zip')

        extension_zip_build_dir = os.path.join(dot_uip_dir, 'dist', build_dir)
        io.make_dir(extension_zip_build_dir)

        if most_recent_file:
            if not zip_filename:
                zip_filename = os.path.basename(most_recent_file)
            zip_filename = os.path.join(extension_zip_build_dir, zip_filename)
            io.remove_file(zip_filename)
            os.rename(most_recent_file, zip_filename)
            return zip_filename
        else:
            raise customexceptions.BuildError(304)
    else:
        raise customexceptions.InvalidFolderError(309, dot_uip_dir)


def build_full_package():
    dot_uip_dir = os.getcwd()
    if is_valid_dot_uip_and_extension_template_dir(dot_uip_dir):
        full_package_build_dir = os.path.join(dot_uip_dir, 'dist', 'package_build')
        extension_zip_path = build_extension(build_dir=full_package_build_dir, zip_filename='extension_archive.zip')

        template_json_path = os.path.join(dot_uip_dir, 'src', 'templates', 'template.json')

        template_json_data = io.read_json(template_json_path)

        template_icon_path = os.path.join(dot_uip_dir, 'src', 'templates', 'template_icon.png')
        template_name = template_json_data.get('name')

        template_dist_name = constants.UNIVERSAL_TEMPLATE_DIST_NAME % template_name
        template_dist_name = template_dist_name.replace(' ', '_')
        template_dist_zip = os.path.join(full_package_build_dir, template_dist_name)
        with zipfile.ZipFile(template_dist_zip, 'w') as zf:
            zf.write(template_json_path, arcname=os.path.basename(template_json_path))

            if os.path.exists(template_icon_path):
                zf.write(template_icon_path, arcname=os.path.basename(template_icon_path))

            zf.write(extension_zip_path, arcname=os.path.basename(extension_zip_path))

        # delete extension_archive.zip
        io.remove_file(extension_zip_path)

        most_recent_file = io.get_most_recent_file(full_package_build_dir, '*.zip')
        if os.path.basename(most_recent_file) != template_dist_name:
            raise customexceptions.BuildError(305)
        else:
            return template_dist_zip
    else:
        raise customexceptions.InvalidFolderError(309, dot_uip_dir)


def generate_build(build_all=False):
    if build_all:
        return build_full_package()
    else:
        return build_extension()


def get_dot_uip_config_file_path(relative_to=os.getcwd()):
    config_file_path = os.path.join(relative_to, constants.DOT_UIP_FOLDER_NAME, constants.CONFIG_FILE_DIR_NAME,
                                    constants.CONFIG_FILE_NAME)
    return config_file_path if os.path.exists(config_file_path) else None
