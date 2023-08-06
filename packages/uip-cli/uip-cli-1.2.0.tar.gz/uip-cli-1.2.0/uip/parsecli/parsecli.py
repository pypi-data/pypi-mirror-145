from __future__ import print_function
import argparse
import os
import sys
from datetime import datetime

from colorama import Fore
from uip.cliapis import apis
from uip.config.mergeconfig import get_merged_config
from uip.exceptions import customexceptions
from uip.uipproject import uipproject
from uip.uiptemplates import template
from uip.utils import formatting, io
from uip.constants.constants import TASK_STATUSES


def pack_login_info(userid, password, url):
    """
    Packs the login information into a tuple

    Parameters
    ----------
    userid : str
        Username used to log into the Controller
    password : str
        Password used to log into the Controller
    url : str
        Url used to connect to the Controller

    Returns
    -------
    3-tuple
        Consists of userid, password, url in that order
    """
    return userid, password, url


def call_func(func, *args, **kwargs):
    if func is None:
        return

    try:
        return_dict = func(*args, **kwargs)
        if return_dict and return_dict.get('msg', ''):
            print(Fore.GREEN + return_dict.get('msg'))
    except Exception as e:
        message = formatting.format_error_style(e)
        print(Fore.RED + message)


def parse_init_command(args):
    """
    Parses the init command and performs
    actions accordingly.

    Parameters
    ----------
    args : argparse.Namespace
        The args read by argparser
    """
    mc = get_merged_config('init', args)
    msg = uipproject.initialize_uip(mc.extension_template, mc.variables, mc.dir)
    return {
        'msg': msg
    }


def parse_template_list_command(args):
    mc = get_merged_config('template_list', args)
    chosen_template_name = mc.extension_template_name

    if chosen_template_name:
        extension_templates = template.get_extension_templates([chosen_template_name])
        if len(extension_templates) == 0:
            raise customexceptions.InvalidValueError(502, chosen_template_name)
    else:
        extension_templates = template.get_all_extension_templates()
    table_data = []
    table_headers = None
    separate_each_entry = True
    for extension_template in extension_templates:
        template_name = extension_template.get('template_name')
        template_path = extension_template.get('template_path')
        template_details = template.get_extension_template_details(template_path)
        template_description = template_details['template_description']

        if chosen_template_name == template_name:
            for template_variable in template_details.get('user_defined_variables'):
                variable_name = list(template_variable.keys())[0]
                variable_default = template_variable[variable_name]['default']
                variable_description = template_variable[variable_name]['description']
                table_data.append([variable_name, variable_default, variable_description])
            table_headers = ['Variable Name', 'Default', 'Description']
            separate_each_entry = False
            break
        else:
            table_data.append([template_name, template_description])
            table_headers = ['Extension Template', 'Description'] if table_headers is None else table_headers

    formatting.print_table(table_headers, table_data, separate_each_entry=separate_each_entry)


def parse_build_command(args):
    mc = get_merged_config('build', args)
    generated_file = uipproject.generate_build(build_all=mc.all)
    filename = os.path.basename(generated_file)
    buildpath = os.path.relpath(os.path.dirname(generated_file))

    msg = formatting.format_list_for_printing([filename],
                                              header='The following files were built in "%s"' % buildpath)
    return {
        'msg': msg
    }


def parse_upload_command(args):
    mc = get_merged_config('upload', args)
    login_info = pack_login_info(mc.userid, mc.password, mc.url)

    return_dict = {}
    if mc.all:
        full_package_zip_path = uipproject.get_built_full_package_zip_path()
        return_dict = apis.import_template(template=full_package_zip_path, login_info=login_info)
    else:
        extension_zip_path = uipproject.get_built_extension_zip_path()
        template_name = uipproject.get_template_name_from_template_json()
        return_dict = apis.upload_extension(name=template_name, extension=extension_zip_path,
                                            login_info=login_info)
    return return_dict


def parse_push_command(args):
    mc = get_merged_config('push', args)
    login_info = pack_login_info(mc.userid, mc.password, mc.url)

    generated_file = uipproject.generate_build(build_all=mc.all)

    return_dict = {}
    if mc.all:
        full_package_zip_path = uipproject.get_built_full_package_zip_path()
        return_dict = apis.import_template(template=full_package_zip_path, login_info=login_info)
    else:
        extension_zip_path = uipproject.get_built_extension_zip_path()
        template_name = uipproject.get_template_name_from_template_json()
        return_dict = apis.upload_extension(name=template_name, extension=extension_zip_path,
                                            login_info=login_info)
    return return_dict


def parse_pull_command(args):
    mc = get_merged_config('pull', args)
    login_info = pack_login_info(mc.userid, mc.password, mc.url)

    pull_download_dir = uipproject.get_pull_command_save_dir()
    if pull_download_dir:
        template_name = uipproject.get_template_name_from_template_json()
        return_dict = apis.export_template(name=template_name, login_info=login_info, exclude=True,
                                           save_dir=pull_download_dir)
        if return_dict:
            template_fullpath = return_dict.get('template_fullpath', None)
            if template_fullpath:
                io.extract_zip(template_fullpath, pull_download_dir)
                io.remove_file(template_fullpath)
                changes = uipproject.move_template_json_icon(move_from=pull_download_dir)

                msg = ''

                if not changes['updated_files'] and not changes['new_files']:
                    msg += 'Local files are already up to date'
                else:
                    if changes['updated_files']:
                        msg += formatting.format_list_for_printing(changes['updated_files'],
                                                                   header='The following files were updated')
                    if changes['new_files']:
                        msg += '\n'
                        msg += formatting.format_list_for_printing(changes['new_files'],
                                                                   header='The following new files were pulled')

                return {
                    'msg': msg
                }


def parse_download_command(args):
    mc = get_merged_config('download', args)
    login_info = pack_login_info(mc.userid, mc.password, mc.url)

    temporary_save_dir = uipproject.get_temporary_save_dir()

    if mc.template_name is None:
        mc.template_name = uipproject.get_template_name_from_template_json()

    if temporary_save_dir:
        return_dict = apis.export_template(name=mc.template_name, login_info=login_info, exclude=False,
                                           save_dir=temporary_save_dir)
        if return_dict:
            template_fullpath = return_dict.get('template_fullpath', None)
            changes = uipproject.move_full_package(full_package_path=template_fullpath)
            msg = ''

            if not changes['updated_file'] and not changes['new_file']:
                msg += '"%s" is already up to date' % changes['unchanged_file']
            elif changes['updated_file']:
                msg += formatting.format_list_for_printing([changes['updated_file']],
                                                           header='The following files were updated')
            elif changes['new_file']:
                msg += formatting.format_list_for_printing([changes['new_file']],
                                                           header='The following new files were downloaded')

            return {
                'msg': msg
            }


def parse_task_launch_command(args):
    mc = get_merged_config('task_launch', args)
    login_info = pack_login_info(mc.userid, mc.password, mc.url)
    task_name = mc.task_name 
    no_wait = mc.no_wait

    dir = os.getcwd()

    if uipproject.is_valid_dot_uip_and_extension_template_dir(dir):
        return_dict = apis.list_universal_tasks(login_info, task_name=task_name)
        if return_dict:
            tasks = return_dict.get('tasks', None)
            if tasks:
                return_dict = apis.launch_universal_task(task_name, login_info)
                if return_dict:
                    # Replace all instances of "sys_id" with just "id"
                    info = return_dict.get('info', '')
                    if info:
                        return_dict['info'] = info.replace('sys_id', 'id')

                if no_wait:
                    return {
                        'msg': return_dict['info']
                    }
                elif return_dict:
                    info = return_dict['info']
                    sysId = return_dict['sysId']
                    print(Fore.GREEN + info + Fore.RESET)
                    print('='*len(info))

                    keep_printing = True
                    last_status = None 
                    try:
                        status_description = None  
                        while keep_printing:
                            return_dict = apis.get_universal_task_instances(task_name, login_info, sysId)
                            if return_dict and return_dict.get('instances', None):
                                task_instances = return_dict['instances']

                                if task_instances:
                                    result = task_instances[0]
                                else:
                                    break

                                status = result['status']

                                if status is None:
                                    continue
                                else:
                                    status = status.title()

                                keep_printing = False 
                                if status in [TASK_STATUSES.success, TASK_STATUSES.finished]:
                                    status = Fore.GREEN + status
                                elif status in [TASK_STATUSES.failed, TASK_STATUSES.cancelled, TASK_STATUSES.start_failure, TASK_STATUSES.undeliverable]:
                                    status = Fore.RED + status 
                                elif status in [TASK_STATUSES.in_doubt, TASK_STATUSES.skipped]:
                                    status = Fore.CYAN + status 
                                else:
                                    status = Fore.YELLOW + status 
                                    keep_printing = True 

                                status = status + Fore.RESET 

                                if last_status and len(last_status) > len(status):
                                    status = status.ljust(len(last_status))

                                print('Status: %s' % status, end='\r')
                                last_status = status 

                                status_description = result['statusDescription']
                                if status_description:
                                    status_description = status_description.strip()
                            else:
                                keep_printing = False
                        else:
                            print('')
                            if status_description:
                                print('Status Description: %s' % status_description)

                        print('='*len(info))  
                        print('\n')
                        if sysId:
                            return_dict = apis.get_task_output(sysId, login_info)
                            if return_dict:
                                if type(return_dict['output']) == list:
                                    all_output = return_dict['output']
                                    for output in all_output:
                                        output_type = '%s Output:' % output['outputType']
                                        print(Fore.BLUE + output_type + Fore.RESET)
                                        print('=' * len(output_type))
                                        print('%s\n' % output['outputData'])
                                else:
                                    print(Fore.BLUE + 'Output:' + Fore.RESET)
                                    print('='*7)
                                    print('%s\n' % return_dict['output'])

                    except KeyboardInterrupt as ki:
                        print('')
                        sys.exit(1)
            else:
                raise customexceptions.InvalidValueError(503, task_name)
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def parse_task_status_command(args):
    mc = get_merged_config('task_status', args)
    login_info = pack_login_info(mc.userid, mc.password, mc.url)
    task_name = mc.task_name 
    num_instances = mc.num_instances

    dir = os.getcwd()

    if uipproject.is_valid_dot_uip_and_extension_template_dir(dir):
        return_dict = apis.list_universal_tasks(login_info, task_name)
        if return_dict:
            tasks = return_dict.get('tasks', None)
            if tasks:
                return_dict = apis.get_universal_task_instances(task_name, login_info)
                if return_dict and return_dict.get('instances', None):
                    task_instances = return_dict['instances']
                    result = list(map(lambda data: {'launchTime': data['launchTime'][:19], 'status': data['status'].title(), 
                                                    'instanceNumber': data['instanceNumber'],
                                                    'sysId': data['sysId'], 'statusDescription': data['statusDescription'],
                                                    'exitCode': data['exitCode']}, task_instances))
                    result.sort(key=lambda data: data['instanceNumber'], reverse=True)

                    table_headers = ['Instance Number', 'Instance Id', 'Launch Time', 'Status (Exit Code)', 'Status Description']
                    table_data = []

                    num_instances = len(result) if num_instances <= 0 else num_instances

                    for data in result[:num_instances]:
                        status = data['status']
                        if status in [TASK_STATUSES.success, TASK_STATUSES.finished]:
                            status = Fore.GREEN + status
                        elif status in [TASK_STATUSES.failed, TASK_STATUSES.cancelled, TASK_STATUSES.start_failure, TASK_STATUSES.undeliverable]:
                            status = Fore.RED + status 
                        elif status in [TASK_STATUSES.in_doubt, TASK_STATUSES.skipped]:
                            status = Fore.CYAN + status 
                        else:
                            status = Fore.YELLOW + status 

                        status = status + Fore.RESET + (' (%s)' % data['exitCode'])
                        statusDescription = data['statusDescription'] or 'N/A'
                        table_data.append([data['instanceNumber'], data['sysId'], data['launchTime'], status, statusDescription])

                    formatting.print_table(table_headers, table_data, separate_each_entry=True)
            else:
                raise customexceptions.InvalidValueError(503, task_name)
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def parse_task_output_command(args):
    mc = get_merged_config('task_output', args)
    login_info = pack_login_info(mc.userid, mc.password, mc.url)
    task_name = mc.task_name 
    instance_number = mc.instance_number
    
    dir = os.getcwd()
    if uipproject.is_valid_dot_uip_and_extension_template_dir(dir):
        return_dict = apis.list_universal_tasks(login_info, task_name)
        if return_dict:
            tasks = return_dict.get('tasks', None)
            if tasks:
                return_dict = apis.get_universal_task_instances(task_name, login_info)
                if return_dict and return_dict.get('instances', None):
                    task_instances = return_dict['instances']
                    result = list(map(lambda data: {'instanceNumber': data['instanceNumber'],
                                                    'sysId': data['sysId']}, task_instances))
                    result.sort(key=lambda data: data['instanceNumber'], reverse=True)

                    if instance_number is None:
                        selected_instance = [result[0]]
                    else:
                        selected_instance = list(filter(lambda data: data['instanceNumber'] == instance_number, result))

                    if selected_instance:
                        selected_instance = selected_instance[0]
                        sysId = selected_instance['sysId']
                        if sysId:
                            return_dict = apis.get_task_output(sysId, login_info)
                            if return_dict:
                                if type(return_dict['output']) == list:
                                    all_output = return_dict['output']
                                    for output in all_output:
                                        output_type = '%s Output:' % output['outputType']
                                        print(Fore.BLUE + output_type + Fore.RESET)
                                        print('=' * len(output_type))
                                        print('%s\n' % output['outputData'])
                                else:
                                    print(Fore.BLUE + 'Output:' + Fore.RESET)
                                    print('='*7)
                                    print('%s\n' % return_dict['output'])
                    else:
                        raise customexceptions.TaskInstanceError(504, instance_number)
            else:
                raise customexceptions.InvalidValueError(503, task_name)
    else:
        raise customexceptions.InvalidFolderError(309, dir)


def parse_task_command(args):
    task_action = args.task_action 
    function_name = 'parse_task_%s_command' % task_action
    func = getattr(sys.modules[__name__], function_name, None)
    call_func(func, args)


def parse_cli_args(args):
    """
    Parses the cli arguments based on the command_type
    argument which is guaranteed to be one of 'extension'
    or 'template', and calls the appropriate function with
    the name 'parse_%s_command' where %s is one of 'extension'
    or 'template'

    Note that this restricts all command_type related arguments
    to be of the form 'parse_%s_commmand'

    Parameters
    ----------
    args : argparse.Namespace
        The args read by argparser
    """
    command = args.command_type
    function_name = 'parse_%s_command' % command
    function_name = function_name.replace('-', '_')
    func = getattr(sys.modules[__name__], function_name, None)
    call_func(func, args)
