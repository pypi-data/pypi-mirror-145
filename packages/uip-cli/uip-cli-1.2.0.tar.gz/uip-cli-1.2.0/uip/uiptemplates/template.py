import os

from uip.constants import constants
from uip.utils import io

from .. import package_dir


def copy_template(template_path, dst):
    io.copy_tree(template_path, dst)
    template_config_yml = os.path.join(dst, constants.TEMPLATE_CONFIG_YAML)
    io.remove_file(template_config_yml)


def copy_resources(resources_to_copy, dst):
    if resources_to_copy:
        resources_to_copy = [resources_to_copy] if type(resources_to_copy) == str else resources_to_copy
        resources_dir = os.path.join(package_dir, constants.RESOURCES_DIR)
        for resource in resources_to_copy:
            resource_path = os.path.join(resources_dir, resource)
            if os.path.isdir(resource_path):
                io.copy_tree(resource_path, dst)
            elif os.path.isfile(resource_path):
                io.copy_file(resource_path, dst)


def get_extension_template_details(template_path):
    if not template_path.endswith(constants.TEMPLATE_CONFIG_YAML):
        template_path = os.path.join(template_path, constants.TEMPLATE_CONFIG_YAML)
    if os.path.exists(template_path):
        template_details = io.read_yaml(template_path)
        return template_details
    else:
        return None


def get_extension_templates(templates_to_get=[]):
    # if templates_to_get is an empty list, all templates will be retrieved
    uiptemplates = os.path.join(package_dir, 'uiptemplates')
    return_list = []
    if os.path.exists(uiptemplates):
        template_folders = [folder for folder in os.listdir(uiptemplates) if
                            os.path.isdir(os.path.join(uiptemplates, folder)) and folder.endswith('templates')]
        for template_folder in template_folders:
            template_folder_path = os.path.join(uiptemplates, template_folder)
            extension_templates = [template for template in os.listdir(template_folder_path) if
                                   os.path.isdir(os.path.join(template_folder_path, template))]
            for extension_template in extension_templates:
                if extension_template in templates_to_get or len(templates_to_get) == 0:
                    if constants.TEMPLATE_CONFIG_YAML in os.listdir(
                            os.path.join(template_folder_path, extension_template)):
                        return_list.append({
                            'template_name': extension_template,
                            'template_path': os.path.join(template_folder_path, extension_template)
                        })
    return return_list


def get_all_extension_templates():
    return get_extension_templates(templates_to_get=[])
