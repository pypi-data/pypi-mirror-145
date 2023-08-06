import errno
import os
import re

from uip.constants import constants
from uip.utils import io

import requests
from uip.exceptions import customexceptions

command_endpoints = {
    'extension': {
        'download': 'extension',
        'upload': 'extension',
    },
    'template': {
        'export': 'exporttemplate',
        'import': 'importtemplate'
    },
    'task': {
        'launch': 'ops-task-launch',
        'status': 'list',
        'list': 'list',
        'output': 'retrieveoutput'
    }
}


def format_url(url, command_type, command):
    """
    Formats the url based on the command being used

    Parameters
    ----------
    url : str
        The url used to connect to the Controller
    command_type : str
        The type of command to get the url endpoint for
    command :
        The command being executed. Must be in `command_endpoints` dict

    Raises
    ------
    customexceptions.KeyNotFoundError
        When url endpoint is not found in the `command_endpoints` dict
    customexceptions.InvalidValueError
        When url is None or empty string

    Returns
    -------
    formatted_url : str
        The formatted url
    """

    if url is None or len(url.strip()) == 0:
        raise customexceptions.InvalidValueError(5)

    formatted_url = url
    if not formatted_url.endswith('/'):
        formatted_url += '/'

    possible_commands = command_endpoints.get(command_type, None)
    if possible_commands is None:
        raise customexceptions.KeyNotFoundError(6, command)

    command_endpoint = possible_commands.get(command, None)
    if command_endpoint is None:
        raise customexceptions.KeyNotFoundError(7, command)
    else:
        url_endpoint = constants.UNIVERSAL_TEMPLATE_URL_ENDPOINT
        if command_type == 'task':
            if command in ['launch', 'list']:
                url_endpoint = constants.TASK_URL_ENDPOINT
            elif command in ['status', 'output']:
                url_endpoint = constants.TASK_INSTANCE_URL_ENDPOINT

        formatted_url += '%s/%s' % (url_endpoint, command_endpoint)
        return formatted_url


def add_template_param(params, name):
    """
    Helper method that adds `name` to `params`

    Parameters
    ----------
    params : dict
        The dictionary to populate with name
    name : str
        The name of the template

    Raises
    ------
    customexceptions.InvalidValueError
        When template name is not specified or params dictionary is None

    Returns
    -------
    None
    """
    if params is None:
        raise customexceptions.InvalidValueError(2)

    if name:
        params['templatename'] = name
    else:
        raise customexceptions.InvalidValueError(4)


def get_request(url, params, auth, stream=False, **kwargs):
    """
    Performs a HTTP get request based on the parameters supplied

    Parameters
    ----------
    url : str
        The url to request data from
    params : dict
        The fields required by the API to successfully return the data
    auth : tuple
        Consists of userid and password in that order as a tuple
    stream : bool, optional
        Whether to stream the data or not, by default False

    Raises
    ------
    customexceptions.InvalidValueError
        When url or params or auth are None

    Returns
    -------
    response : requests.models.Response
        Response object containing the results of the request
    """

    if url is None or len(url.strip()) == 0:
        raise customexceptions.MissingValueError(5)
    elif params is None:
        raise customexceptions.InvalidValueError(2)
    elif auth is None:
        raise customexceptions.InvalidValueError(1)

    response = requests.get(url=url, auth=auth, params=params, stream=stream, **kwargs)
    return response


def post_request(url, auth, params=None, payload=None, **kwargs):
    """
    Performs a HTTP post request based on the parameters supplied

    Parameters
    ----------
    url : str
        The url to post data to
    auth : tuple
        Consists of userid and password in that order as a tuple
    params : dict, optional
        The fields, if required by the API, to successfully post data, by default None
    payload : file, optional
        The data, if specified, to upload with the post request, by default None

    Raises
    ------
    customexceptions.InvalidValueError
        When url or auth are None

    Returns
    -------
    response : requests.models.Response
        Response object containing the results of the request
    """
    if url is None or len(url.strip()) == 0:
        raise customexceptions.MissingValueError(5)
    elif auth is None:
        raise customexceptions.InvalidValueError(1)

    if payload:
        response = requests.post(url=url, auth=auth, params=params, data=payload, **kwargs)
    else:
        response = requests.post(url=url, auth=auth, params=params, **kwargs)
    return response


def extract_filename_from_resp(response, default_filename=None):
    """
    Extracts the filename from the supplied response object. If not possible,
    then the default_filename parameter is returned instead.

    Parameters
    ----------
    response : requests.models.Response
        Response object used to extract the filename
    default_filename : str, optional
        If filename is not in Response object, then default_filename is used,
        by default None

    Raises
    ------
    customexceptions.InvalidValueError
        When response is None

    Returns
    -------
    filename : str
        The extracted filename
    """

    if response is None:
        raise customexceptions.InvalidValueError(3)

    filename = default_filename
    if response.ok:
        content_disposition = response.headers.get('Content-Disposition', None)
        if content_disposition:
            res = re.findall("filename=\"(.+)\"", content_disposition)
            if res:
                filename = res[0]
    return filename


def write_to_file(content, filepath):
    """
    Writes the specified content to the file specified.
    If the directory the file resides in does not exists,
    it is automatically created.

    Parameters
    ----------
    content : any form of data (tuple, dict, str etc.)
        The content to write to the file
    filepath : str
        Path to the file to write to
    """
    if filepath and content:
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            if dirname:
                io.make_dir(dirname)
        with open(filepath, 'wb') as f:
            f.write(content)


def download_extension(name, login_info, save_dir="."):
    """
    Downloads a specified extension, and saves it to a custom directory (if specified),
    or to the current working directory

    Parameters
    ----------
    name : str
        Name of the template which contains the extension to download
    save_dir : str
        Full path of the directory to download the file to 
    login_info : 3-tuple
        Consists of userid, password, and url in that order

    Raises
    ------
    customexceptions.ControllerRequestError
        When the response object's status code is not OK

    Returns
    -------
    dict
        If successful, returns a success message along with extension filename and fullpath to zip
    """
    userid, password, url = login_info
    download_url = format_url(url, 'extension', 'download')

    params = {}
    add_template_param(params, name)

    auth = (userid, password)

    response = get_request(download_url, params, auth, stream=True)
    if response.ok:
        filename = extract_filename_from_resp(response, default_filename='extension.zip')
        fullpath = os.path.join(save_dir, filename)
        write_to_file(response.content, fullpath)
        return {
            'msg': "Successfully downloaded Extension (%s) from Universal Template '%s'" % (fullpath, name),
            'extension_filename': filename,
            'extension_fullpath': fullpath
        }
    else:
        raise customexceptions.ControllerRequestError(response)


def upload_extension(name, extension, login_info):
    """
    Uploads an extension zip file to the specified template

    Parameters
    ----------
    name : str
        Name of the template to upload the Extension to
    extension : str
        Name of the zip file to upload
    login_info : 3-tuple
        Consists of userid, password, and url in that order

    Raises
    ------
    customexceptions.FileNotFoundError
        When the specified extension zip file is not found
    customexceptions.ControllerRequestError
        When the response object's status code is not OK

    Returns
    -------
    dict
        If successful, returns the message from the post request response
    """
    userid, password, url = login_info
    upload_url = format_url(url, 'extension', 'upload')

    params = {}
    add_template_param(params, name)

    auth = (userid, password)

    try:
        with open(extension, 'rb') as data:
            response = post_request(upload_url, auth, params=params, payload=data)
    except IOError as e:
        if e.errno == errno.ENOENT:
            raise customexceptions.FileNotFoundError(8, extension)
        else:
            raise

    if response and response.ok:
        return {
            'msg': response.text,
        }
    else:
        raise customexceptions.ControllerRequestError(response)


def export_template(name, login_info, exclude=False, save_dir='.'):
    """
    Download the specified template and save it to a custom directory (if specified).
    If exclude is True, the extension is excluded from the download

    Parameters
    ----------
    name : str
        Name of the template to download
    exclude : bool
        indicates whether to exclude the extension from template or not
    save_dir : str
        Path to the directory to save the template to
    login_info : 3-tuple
        Consists of userid, password, and url in that order

    Raises
    ------
    customexceptions.ControllerRequestError
        When the response object's status code is not OK

    Returns
    -------
    dict
        If successful, returns a success message along with template filename and fullpath to zip
    """
    userid, password, url = login_info
    export_url = format_url(url, 'template', 'export')

    params = {}
    add_template_param(params, name)
    params['excludeExtension'] = exclude

    auth = (userid, password)

    response = get_request(export_url, params, auth, stream=True)
    if response.ok:
        filename = extract_filename_from_resp(response, default_filename='template.zip')
        fullpath = os.path.join(save_dir, filename)
        write_to_file(response.content, fullpath)
        return {
            'msg': "Successfully downloaded Universal Template (%s)" % fullpath,
            'template_fullpath': fullpath,
            'template_filename': filename
        }
    else:
        raise customexceptions.ControllerRequestError(response)


def import_template(template, login_info):
    """
    Upload the specified template to the Controller

    Parameters
    ----------
    template : str
        Name of the template zip to upload
    login_info : 3-tuple
        Consists of userid, password, and url in that order

    Raises
    ------
    customexceptions.FileNotFoundError
        When the specified template zip file is not found
    customexceptions.ControllerRequestError
        When the response object's status code is not OK

    Returns
    -------
    dict
        If successful, returns the message from the post request response
    """
    userid, password, url = login_info
    import_url = format_url(url, 'template', 'import')

    auth = (userid, password)

    try:
        with open(template, 'rb') as data:
            response = post_request(import_url, auth, payload=data)
    except IOError as e:
        if e.errno == errno.ENOENT:
            raise customexceptions.FileNotFoundError(8, template)
        else:
            raise

    if response and response.ok:
        return {
            'msg': response.text
        }
    else:
        raise customexceptions.ControllerRequestError(response)


def list_universal_tasks(login_info, task_name = None):
    userid, password, url = login_info
    list_url = format_url(url, 'task', 'list')
    
    auth = (userid, password)

    filters = {"type": "Universal"}
    
    if task_name:
        filters.update({"name": task_name})

    response = post_request(list_url, auth, json=filters, headers={"accept": "application/json"})

    if response and response.ok:
        return {
            'tasks': response.json()
        }
    else:
        raise customexceptions.ControllerRequestError(response)


def launch_universal_task(task_name, login_info):
    userid, password, url = login_info
    launch_url = format_url(url, 'task', 'launch')
    
    auth = (userid, password)

    response = post_request(launch_url, auth, json={"name": task_name}, headers={"accept": "application/json"})

    if response and response.ok:
        result = response.json()
        info = result.get('info', None)
        sysId = result.get('sysId', None)
        if info and sysId:
            return {
                'info': info,
                'sysId': sysId
            }
        else:
            raise customexceptions.TaskLaunchError(response)
    else:
        raise customexceptions.ControllerRequestError(response)


def get_universal_task_instances(task_name, login_info, sysId=None):
    userid, password, url = login_info
    status_url = format_url(url, 'task', 'status')
    
    auth = (userid, password)

    if sysId:
        response = post_request(status_url, auth, json={"type": "Universal", "sysId": sysId}, headers={"accept": "application/json"})
    else:
        response = post_request(status_url, auth, json={"name": "*", "type": "Universal", "taskName": task_name}, headers={"accept": "application/json"})

    if response and response.ok:
        result = response.json()
        if result:
            return {
                'instances': result 
            }
        else:
            raise customexceptions.TaskInstanceError(9, task_name)
    else:
        raise customexceptions.ControllerRequestError(response)


def get_task_output(task_instance_id, login_info):
    userid, password, url = login_info
    output_url = format_url(url, 'task', 'output')
    
    auth = (userid, password)

    params = {'taskinstanceid': task_instance_id}
    response = get_request(output_url, params, auth, headers={"accept": "application/json"})
    if response and response.ok:
        result = response.json()
        if result:
            return {
                'output': result 
            }
    elif response.text:
        return {
            'output': response.text
        }
    else:
        raise customexceptions.ControllerRequestError(response)