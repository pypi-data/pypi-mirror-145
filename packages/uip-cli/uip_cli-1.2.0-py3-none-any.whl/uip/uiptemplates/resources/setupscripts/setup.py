#!/usr/bin/env python

import os
import glob
import yaml

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from distutils.util import convert_path
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

EXTENSION_SRC_DIR = 'src'
THIRD_PARTY_SRC_DIR = '3pp'
THIRD_PARTY_PACKAGE = THIRD_PARTY_SRC_DIR.split('/')[-1]


class build_py(_build_py):
    """Override setuptools's build_py class to implement additional
    logic to support extension packaging.
    """

    def get_module_outfile(self, build_dir, package, module):
        """Third party folder normally contains packages but it
        can also contains standalone modules such as six.py,
        for these modules we will move it to the root of the
        zip file to maintain consistency.
        """
        if package == [THIRD_PARTY_PACKAGE]:
            outfile_path = [build_dir] + [module + ".py"]
        else:
            outfile_path = [build_dir] + list(package) + [module + ".py"]

        return os.path.join(*outfile_path)


class bdist_egg(_bdist_egg, object):
    """Override setuptools's bdist_egg class to implement additional
    logic to support extension packaging.
    """

    def finalize_options(self):
        """Rename .egg extension to .zip"""
        super(bdist_egg, self).finalize_options()
        self.egg_output = '.'.join(
            [os.path.splitext(self.egg_output)[0], 'zip'])


def find_modules(where, package=None):
    """Find and return list of Python modules.

    Args:
        where (str): path to search for module files
        package (str): if specified, this will append to the modules name
                       in the output list
    Returns:
        Return list of modules, empty list is return if no modules
        is found under the search path
    """
    module_files = []

    for file in glob.glob(os.path.join(where, "*.py")):
        module = os.path.splitext(os.path.basename(file))[0]

        if package is None:
            module_files.append(module)
        else:
            module_files.append('.'.join([package, module]))

    return module_files


def get_package_dir():
    """Return dict object contains full list of packages to be packaged"""
    # pacakge: dir, package is separated by . and dir is separated by /
    package_dir = {'': EXTENSION_SRC_DIR,
                   THIRD_PARTY_PACKAGE: THIRD_PARTY_SRC_DIR}

    # distutil convert_path automatically convert / to native os path separator
    # so just use / here regardless of os.sep
    package_dir.update({package: '{}/{}'.format(THIRD_PARTY_SRC_DIR,
                                                package.replace('.', '/'))
                        for package in find_packages(THIRD_PARTY_SRC_DIR)})

    return package_dir


# load meta data
with open('{}/extension.yml'.format(EXTENSION_SRC_DIR), 'r') as file:
    meta = yaml.load(file, Loader=Loader)

setup(name=meta['extension']['name'],
      version=meta['extension']['version'],
      description=meta.get('extension', {}).get('description', ''),
      author=meta.get('owner', {}).get('name', ''),
      author_email=meta.get('owner', {}).get('email', ''),
      url="https://stonebranch.com",
      license="Copyright 2022, Stonebranch Inc, All Rights Reserved.",
      package_dir=get_package_dir(),
      packages=find_packages(THIRD_PARTY_SRC_DIR),
      include_package_data=True,
      py_modules=find_modules(EXTENSION_SRC_DIR)
      + find_modules(THIRD_PARTY_SRC_DIR, THIRD_PARTY_PACKAGE),
      data_files=[('', ['{}/extension.yml'.format(EXTENSION_SRC_DIR)])],
      cmdclass={'build_py': build_py, 'bdist_egg': bdist_egg})
