import glob
import hashlib
import json
import os
import shutil
import zipfile
from distutils import dir_util

import yaml


def read_yaml(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    else:
        return None


def read_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    else:
        return None


def read_user_input(prompt):
    try:
        input_prompt = raw_input
    except NameError:
        input_prompt = input

    return input_prompt(prompt)


def read_user_choice(message, choice_list):
    if not choice_list or len(choice_list) == 0:
        return None

    print(message)
    for index, value in enumerate(choice_list):
        print(('  (%d) %s' % ((index + 1), value)))
    print('')

    user_choice = -1
    while user_choice < 1 or user_choice > len(choice_list):
        user_choice = read_user_input('Please type the number of one of the choices presented above: ')
        try:
            user_choice = int(user_choice)
        except ValueError:
            user_choice = -1
            pass

    return choice_list[user_choice - 1]


def get_most_recent_file(dir, filetype='*'):
    if dir and os.path.exists(dir):
        if not filetype.startswith('*.'):
            filetype = '*.%s' % filetype
        files = glob.glob(os.path.join(dir, filetype))
        return max(files, key=os.path.getctime) if files else None
    else:
        return None


def get_files_of_specific_type(dir, filetype):
    if os.path.exists(dir):
        if not filetype.startswith('*.'):
            filetype = '*.%s' % filetype
        return glob.glob(os.path.join(dir, filetype))
    else:
        return None


def get_md5_of_zipfile(zip_filepath):
    if zip_filepath and os.path.exists(zip_filepath) and zipfile.is_zipfile(zip_filepath):
        md5 = hashlib.md5()
        with zipfile.ZipFile(zip_filepath, 'r') as zf:
            for f in zf.infolist():
                md5.update(str(f.CRC).encode('utf-8'))
        return md5.hexdigest()
    else:
        return None


def get_md5_of_file(filepath):
    if filepath and os.path.exists(filepath):
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()
    else:
        return None


def extract_zip(zip_filepath, extract_dir):
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        zf.extractall(extract_dir)


def remove_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)


def remove_file(file):
    if os.path.exists(file):
        os.remove(file)


def copy_tree(src, dst):
    if os.path.exists(src):
        dir_util.copy_tree(src, dst)


def copy_file(src, dst):
    if os.path.exists(src) and os.path.isfile(src):
        shutil.copy(src, dst)

def write_to_file(dst_file, contents):
    with open(dst_file, 'w+') as f:
        f.write(contents)

def make_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
