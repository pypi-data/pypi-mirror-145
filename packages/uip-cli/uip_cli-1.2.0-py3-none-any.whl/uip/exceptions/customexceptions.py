import argparse

import requests
from uip.exceptions.errormessages import error_messages


def format_error(error_num, *vars):
    error_message = error_messages[error_num]
    return error_message.format(*vars) if vars else error_message


class KeyNotFoundError(KeyError):
    """
    Class used to report errors related to key 
    not found in a dictionary

    Parameters
    ----------
    KeyError : Exception
        Superclass
    """

    def __init__(self, error_num, *vars):
        super(KeyNotFoundError, self).__init__(format_error(error_num, *vars))


class InvalidValueError(ValueError):
    """
    Class used to report errors related to 
    invalid values

    Parameters
    ----------
    ValueError : Exception
        Superclass
    """

    def __init__(self, error_num, *vars):
        super(InvalidValueError, self).__init__(format_error(error_num, *vars))


class MissingValueError(ValueError):
    def __init__(self, error_num, *vars):
        super(MissingValueError, self).__init__(format_error(error_num, *vars))


class InvalidArgTypeError(argparse.ArgumentTypeError):
    """
    Class used to report errors related to invalid 
    argument types for argparse modules

    Parameters
    ----------
    argparse.ArgumentTypeError : Exception
        Superclass
    """

    def __init__(self, error_num, *vars):
        super(InvalidArgTypeError, self).__init__(format_error(error_num, *vars))


class FileNotFoundError(IOError):
    """
    Class used to report errors related to file 
    not being found. Note that this error is implemented
    in Python >=3 by default, but implementing our own 
    version will not cause problems

    Parameters
    ----------
    IOError : Exception
        Superclass
    """

    def __init__(self, error_num, *vars):
        super(FileNotFoundError, self).__init__(format_error(error_num, *vars))


class ControllerRequestError(requests.exceptions.HTTPError):
    """
    Class used to report errors related to get/post requests
    sent to the Controller

    Parameters
    ----------
    requests.exceptions.HTTPError : Exception
        Superclass
    """

    def __init__(self, response):
        message = 'Status %d: ' % response.status_code
        content_length = int(response.headers.get('Content-Length', 0))

        if content_length:
            content_type = response.headers.get('Content-Type', None)
            if content_type and 'text/plain' in content_type:
                message += response.text
            else:
                message += 'Could not connect to the Controller. Check the url'
        else:
            message += 'Could not connect to the Controller. Check userid and password'

        super(ControllerRequestError, self).__init__(message)


class TaskLaunchError(Exception):
    def __init__(self, response):
        result = response.json()
        message = ''
        if result:
            message = result.get('errors', '')
        super(TaskLaunchError, self).__init__(message)


class TaskInstanceError(Exception):
    def __init__(self, error_num, *vars):
        super(TaskInstanceError, self).__init__(format_error(error_num, *vars))


class InvalidFolderError(IOError):
    def __init__(self, error_num, *vars):
        super(InvalidFolderError, self).__init__(format_error(error_num, *vars))


class BuildError(IOError):
    def __init__(self, error_num, *vars):
        super(BuildError, self).__init__(format_error(error_num, *vars))


class CorruptedFileError(IOError):
    def __init__(self, error_num, *vars):
        super(CorruptedFileError, self).__init__(format_error(error_num, *vars))


class Error(Exception):
    def __init__(self, error_num, *vars):
        super(Error, self).__init__(format_error(error_num, *vars))


class InitError(IOError):
    def __init__(self, error_num, *vars):
        super(InitError, self).__init__(format_error(error_num, *vars))

class PlatformError(IOError):
    def __init__(self, error_num, *vars):
        super(PlatformError, self).__init__(format_error(error_num, *vars))