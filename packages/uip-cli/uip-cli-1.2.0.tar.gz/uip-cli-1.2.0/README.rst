Universal Integration Platform Command Line Utility
===================================================

Overview
========
``uip-cli`` is a command line utility by Stonebranch Inc. that is used
to interface with the Universal Extension Web Service APIs. The goal of
the CLI is to make the process of creating, editing, and deploying
Extensions convenient and fast.

Features
--------

-  Quickly prototype Extensions using starter Extension Templates
-  Build and upload Extensions and/or Universal Templates
-  Pull the latest Universal Template source files from the Controller
-  Download the full Universal Template package 

Getting Started
===============
Requirements
------------

``uip-cli`` works with Python 2.7 and greater on Windows, Linux, and
MacOS, and uses the following third party libraries:

- ``colorama`` (0.4.4)
- ``requests`` (2.26.0) 
- ``jinja2`` (2.11.3) 
- ``prettytable`` (1.0.1)
- ``pyyaml`` (5.4.1)
- ``setuptools`` (44.1.1)

All the required libraries listed above are automatically installed
during the installation process

Installation
------------

To install ``uip-cli``, download it from `PyPI <https://pypi.org/>`_ and install it with ``pip``.
To ensure proper installation/upgrade, the version of ``pip`` installed should be 20.0.1 or greater.

The ``setuptools`` module, which should already be installed with ``pip`` is required to install 
``uip-cli``. To ensure a smooth installation,  we recommend using ``setuptools`` version 44.1.1 
or greater.

To upgrade ``pip`` and ``setuptools`` prior to installing ``uip-cli``, enter the following command:
::
  
    $ python -m pip install --upgrade pip setuptools

To install: 
::
    
    $ pip install uip-cli

To upgrade:
::

    $ pip install uip-cli --upgrade 

The CLI is installed as ``uip``. To confirm it is installed properly, type the following:
::
    
    $ uip 

and you should see something similar to:
:: 

    usage: uip [-h] <command> ...

    optional arguments:
    -h --help
                    show this help message and exit

    commands:
    <command>
        init         initialize a new project with starter Extension templates
        template-list
                     list of available Extension templates
        build        used to build Extension or full package
        upload       upload Extension (or full package) to the Controller
        push         build and upload Extension (or full package) to the Controller
        pull         pulls the latest template.json (and template_icon.png, if
                     present)
        download     downloads the full Universal Template package
        task         used to perform actions on Universal Extension tasks

    examples:
    uip <command>
    uip init
    uip download

Basic Usage 
===========
``uip-cli`` currently supports the following commands:

- init 
- template-list
- build 
- upload 
- push 
- pull 
- download
- task

  - launch
  - status   
  - output

A brief overview of each of the commands is provided below along with 
some examples. For a more detailed demonstration of the commands, 
refer to the 'How-To/Getting Started' Document. 

``init`` 
--------
This command is used to initialize a new project using one of the provided 
starter Extension templates. It can also be used to initialize an existing,
*partially valid* Extension project.

**To initialize a brand new project using a starter Extension template, issue the 
following command**:
:: 

    $ uip init -t ue-task -e 'extension_name=my_sample_extension'


- The ``-t`` option accepts the name of the starter Extension template. For a full 
  list of the available Extension templates, see the ``template-list`` command below. 
- The ``-e`` option is used to configure the starter Extension template with user-defined 
  variables. See the ``template-list`` command for instructions on obtaining 
  a full list of configurable variables. 

Once the CLI executes the command, a project will be initialized in the current 
working directory with the following structure:
::

    |   setup.cfg
    |   setup.py
    |   __init__.py
    |
    |---.uip
    |   |---config
    |           uip.yml
    |
    |---src
        |   extension.py
        |   extension.yml
        |   __init__.py
        |
        |---templates
                template.json


Note that the file system layout above demonstrates a complete, valid Extension project.


Users who created an Extension project outside of ``uip-cli`` (e.g., the project structure
was created manually following instructions in the How-To/Getting Started guide) will not
have the  ``.uip`` folder. Such a directory structure is *partially valid*. 

**To convert an existing, partially valid Extension project into a fully valid one, 
issue the following command:**

:: 

    $ uip init 

The CLI will first check to make sure ``extension.py``, ``extension.yml``, and ``template.json``
exist in their respective directories shown above. If so, the CLI will create the ``.uip`` folder.
Additionally, if ``setup.py`` and ``setup.cfg`` are not present, they will be created along with the
``.uip`` folder.


``template-list`` 
-----------------
This command is used to list all the available starter Extension templates as well as 
the variables used to configure the templates. 

To see the list of available templates, type the following:
::

    $ uip template-list 

Something similar to the output below should be shown:
:: 

    +--------------------+---------------------------------------------------------+
    | Extension Template | Description                                             |
    +--------------------+---------------------------------------------------------+
    | ue-publisher       | starter Extension with a local Universal Event template |
    +--------------------+---------------------------------------------------------+
    | ue-task            | starter Extension with minimal code                     |
    +--------------------+---------------------------------------------------------+

To see the list of configurable variables for one of the templates shown above, 
type the following (same process applies to ``ue-publisher``): 
:: 

    $ uip template-list ue-task 

and a table of variables will be shown: 
:: 

    +---------------------------+------------------+--------------------------------+
    | Variable Name             | Default          | Description                    |
    +---------------------------+------------------+--------------------------------+
    | extension_name            | ue-task          | Extension name                 |
    | extension_version         | 1.0.0            | Extension version              |
    | extension_api_level       | 1.1.0            | Extension API level            |
    | extension_requires_python | >=2.6            | Extension Python requirement   |
    | owner_name                | Stonebranch      | Extension owner's name         |
    | owner_organization        | Stonebranch Inc. | Extension owner's organization |
    | universal_template_name   | UE Task          | Universal Template name        |
    +---------------------------+------------------+--------------------------------+


``build`` 
---------
This command is used to build an Extension or the full package.

A full package build consists of the Universal Template and the Extension. 


To build the Extension only:
:: 

    $ uip build 

To build the full package:
:: 

    $ uip build -a 


``upload`` 
----------
This command is used to upload an Extension or the full package to the 
Controller. 

To upload the Extension only:
:: 

    $ uip upload 


``uip-cli`` uploads the Extension to the Universal Template specified in the 
``template.json`` file. If the template.json file is corrupted or name field 
is missing, the upload will fail.

To upload the full package:
:: 

    $ uip upload -a 


``push`` 
--------
This command is a combination of the build and upload command. 

To push the Extension only:
:: 

    $ uip push 


``uip-cli`` pushes the Extension to the Universal Template specified in the 
``template.json`` file. If the template.json file is corrupted or name field 
is missing, the push will fail.

To push the full package (the Universal Template and Extension):
:: 

    $ uip push -a 


``pull`` 
--------
This command is used to pull the Universal Template source files
``template.json`` and ``template_icon.png`` (if present). These files
are placed in the ``src/templates`` folder. 

As with the ``push`` command, ``uip-cli`` obtains the Universal Template name
from the ``template.json`` file that exists in the project directory.
If the ``template.json`` file is corrupted or the name field is missing, the 
pull will fail.


To pull the source files:
::

    $ uip pull 


``download``
------------
This command is used to download the full Universal Template as a zip.  

``uip-cli`` obtains the Universal Template name from the ``template.json`` 
file that exists in the project directory. If the ``template.json`` file 
is corrupted or the name field is missing, the download will fail.

To download the full Universal Template:
::

    $ uip download 

Optionally, it is possible to download another Universal Template by 
specifying the Universal Template name:
:: 

    $ uip download -n <universal template name>


``task``
------------
This command is used to perform actions on Universal Extension tasks. 
As of now, three actions/subcommands are supported: ``launch``, ``status``, 
and ``output`` which allow the CLI to launch, get status, and get output of
Universal Extension tasks. 

All three subcommands must be used in a complete, valid Extension project 
to work.

To launch an Universal Extension task:
::

    $ uip task launch <task name> 

By default, the CLI will launch the task and continuously print the status 
of the task until it succeeds/fails. Upon success/failure, the task output 
will be printed as well. If the ``--no-wait`` option is specified, the CLI 
will exit immediately after launching the task (task status and output will 
NOT be printed). 

To get the status of Universal Extension task instances:
:: 

    $ uip task status <task name>

By default, the CLI will print the status and exit code of the most recent 
task instance of the specified task. The ``--num-instances`` option can be 
used to specify the number of task instances to get the status of. If a 
nonpositive integer is specified, the status of all the instances will be 
printed. 

To get the output of an Universal Extension task instance:
:: 

    $ uip task output <task name>

By default, the CLI will print the output of the most recent task instance
of the specified task. The ``--instance-number`` option can be used to  
specify the number of the task instance to get the output of. 

Configuration 
=============
There are three primary ways to configure the CLI and its commands (listed in order of precedence):

- Command Line Arguments 
- Environment Variables 
- Configuration Files 

Command Line Arguments
----------------------
Similar to most CLI applications, ``uip`` supports both short and long command line arguments. 
The short arguments start with a single dash and long arguments start with two dashes as shown below:
::

    $ uip build -a 
    $ uip build --all 


Environment Variables
---------------------
Most of the options that can be configured through the command line can also be configured using 
environment variables. All environment variables are prefixed with ``UIP_``. 

Configuration Files 
-------------------
The CLI can be configured through two types of configuration files: global and local. 
**The local configuration file has precedence over the global one.** 

**The global configuration file is installed when uip-cli is used for the first time**

- On Windows, the file is located in ``C:\Users\<USER>\AppData\Local\UIP\config`` where 
  ``USER`` is the one who installed the CLI.
- On Linux/MacOS, the file is located in ``~/.config/uip/config`` where ``~`` is the user's 
  home directory.

**The local configuration file is installed with the init command**

As you may have seen in the directory structure above, the ``.uip`` folder contains a 
``config`` folder which houses the local configuration file. Whenever a new project or 
an existing project is initialized using ``init``, the CLI will automatically create the
``.uip`` folder along with the configuration file. This allows separate projects to have
their own set of configurations.

**Configuration file format**

Both the global and local configuration files are called ``uip.yml``. The files must be 
formatted using proper YAML format. See the example below:
::

    userid: admin 
    url: http://localhost:8080/uc 
    build-all: yes 


Full List of Configuration Options 
==================================

Login Options
-------------
.. list-table:: Login Arguments 
   :header-rows: 1

   * - Option Name 
     - Short Arg 
     - Long Arg
     - Environment Variable
     - Configuration File Arg 
     - Default
   * - User ID
     - ``-u``
     - ``--userid``
     - UIP_USERID  
     - userid  
     - None
   * - Password  
     - ``-w``
     - ``--password``
     - UIP_PASSWORD 
     - None
     - None
   * - URL  
     - ``-i``
     - ``--url``
     - UIP_URL 
     - url 
     - None


``init`` command options  
------------------------
.. list-table:: Optional Arguments 
   :header-rows: 1

   * - Option Name 
     - Short Arg 
     - Long Arg
     - Environment Variable
     - Configuration File Arg 
     - Required 
     - Default
   * - Extension Template 
     - ``-t``
     - ``--extension-template``
     - None 
     - None 
     - NO 
     - None
   * - Variables 
     - ``-e``
     - ``--variables``
     - UIP_TEMPLATE_VARIABLES 
     - variables 
     - NO 
     - None 


Values for the **variables** option can be specified in three different ways:

- Using the ``-e`` option multiple times:
  ::

      $ uip init -t ue-task -e 'var1=value1' -e 'var2=value2' -e 'var3=value3'
        
- Using a JSON string:
  ::

      $ uip init -t ue-task -e '{"var1": "value1", "var2": "value2", "var3": "value3"}'

- Using a JSON/YAML file:
  :: 

      $ uip init -t ue-task -e '@vars.yml'

  where ``vars.yml`` contains 
    
  ::

      var1: value1
      var2: value2 
      var3: value3 

  **Note that the filename/filepath must be prefixed with '@'**

.. list-table:: Positional Arguments 
   :header-rows: 1
  
   * - Option Name 
     - Required 
     - Default
     - Description
   * - <dir> 
     - NO 
     - Current Working Directory 
     - Where to initialize the Extension template. For example, in the following command:
       ``uip init -t ue-task -e '@vars.yml' my_extension_dir``, ``my_extension_dir`` is 
       where the ``ue-task`` Extension template will be initialized.


``template-list`` command options  
---------------------------------
.. list-table:: Positional Arguments 
   :header-rows: 1

   * - Option Name 
     - Required 
     - Default
     - Description
   * - <extension template name> 
     - NO 
     - None 
     - The name of the Extension template to get more details of. For example, in the 
       following command: ``uip template-list ue-task``, ``ue-task`` is the value of 
       ``<extension template name>``. 


``build`` command options  
-------------------------
.. list-table:: Optional Arguments 
   :header-rows: 1

   * - Option Name 
     - Short Arg 
     - Long Arg
     - Environment Variable
     - Configuration File Arg 
     - Required 
     - Default
   * - Build All  
     - ``-a``
     - ``--all``
     - UIP_BUILD_ALL 
     - build-all 
     - NO 
     - False


``upload`` command options  
--------------------------
.. list-table:: Optional Arguments 
   :header-rows: 1

   * - Option Name 
     - Short Arg 
     - Long Arg
     - Environment Variable
     - Configuration File Arg 
     - Required 
     - Default
   * - Upload All  
     - ``-a``
     - ``--all``
     - UIP_UPLOAD_ALL 
     - upload-all 
     - NO 
     - False


``push`` command options  
------------------------
.. list-table:: Optional Arguments 
   :header-rows: 1

   * - Option Name 
     - Short Arg 
     - Long Arg
     - Environment Variable
     - Configuration File Arg 
     - Required 
     - Default
   * - Push All  
     - ``-a``
     - ``--all``
     - UIP_PUSH_ALL 
     - push-all 
     - NO 
     - False


``download`` command options  
----------------------------
.. list-table:: Optional Arguments 
   :header-rows: 1

   * - Option Name 
     - Short Arg 
     - Long Arg
     - Environment Variable
     - Configuration File Arg 
     - Required 
     - Default
   * - Template Name   
     - ``-n``
     - ``--template-name``
     - UIP_TEMPLATE_NAME 
     - template-name 
     - NO 
     - Name from ``template.json``


``task launch`` command options  
-------------------------------
.. list-table:: Positional Arguments 
   :header-rows: 1
  
   * - Option Name 
     - Required 
     - Default
     - Description
   * - <task name> 
     - YES
     - None
     - Name of the Universal Extension task to launch

.. list-table:: Optional Arguments 
   :header-rows: 1

   * - Option Name 
     - Short Arg 
     - Long Arg
     - Environment Variable
     - Configuration File Arg 
     - Required 
     - Default
   * - No Wait  
     - ``-N``
     - ``--no-wait``
     - UIP_NO_WAIT 
     - no-wait 
     - NO
     - False


``task status`` command options  
-------------------------------
.. list-table:: Positional Arguments 
   :header-rows: 1
  
   * - Option Name 
     - Required 
     - Default
     - Description
   * - <task name> 
     - YES
     - None
     - Name of the Universal Extension task to get status of 

.. list-table:: Optional Arguments 
   :header-rows: 1

   * - Option Name 
     - Short Arg 
     - Long Arg
     - Environment Variable
     - Configuration File Arg 
     - Required 
     - Default
   * - Num Instances
     - ``-n``
     - ``--num-instances``
     - UIP_NUM_INSTANCES 
     - num-instances
     - NO
     - 1


``task output`` command options  
-------------------------------
.. list-table:: Positional Arguments 
   :header-rows: 1
  
   * - Option Name 
     - Required 
     - Default
     - Description
   * - <task name> 
     - YES
     - None
     - Name of the Universal Extension task to get the output of 

.. list-table:: Optional Arguments 
   :header-rows: 1

   * - Option Name 
     - Short Arg 
     - Long Arg
     - Environment Variable
     - Configuration File Arg 
     - Required 
     - Default
   * - Instance Number
     - ``-s``
     - ``--instance-number``
     - UIP_INSTANCE_NUMBER 
     - instance-number
     - NO
     - most recent task instance
     
License
=======
``uip-cli`` is released under the `GNU General Public License <https://www.gnu.org/licenses/gpl-3.0.en.html>`_

Acknowledgements
================
``uip-cli`` acknowledges the use of the following open source Python modules:

- `colorama <https://pypi.org/project/colorama/>`_ (BSD License)
- `Jinja2 <https://pypi.org/project/Jinja2/>`_ (BSD-3-Clause License)
- `prettytable <https://pypi.org/project/prettytable/>`_ (BSD-3-Clause License)
- `PyYAML <https://pypi.org/project/PyYAML/>`_ (MIT)
- `requests <https://pypi.org/project/requests/>`_ (Apache 2.0)
- `setuptools <https://pypi.org/project/setuptools/>`_ (MIT)

Copyright
=========
Copyright (c) 2022. Stonebranch, Inc. All rights reserved.
