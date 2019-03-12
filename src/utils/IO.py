import json
import os

import shutil

info_file = 'resources/info.json'
config_file = 'config.json'
tmp_folder = 'resources/tmp'


# IO

def check_file(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    if not os.path.isfile(path):
        raise Exception("File not found")


def read_json(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    check_file(path)
    with open(path) as f:
        data = json.load(f)
    return data


def save_json(data, path):
    """
    TODO DOCUMENTATION
    :param data:
    :param path:
    :return:
    """
    with open(path, 'w') as out:
        json.dump(data, out, indent=4, ensure_ascii=False)
    return path


def read_info_file():
    """
    TODO DOCUMENTATION
    :return:
    """
    check_file(info_file)
    return json.load(open(info_file))


def read_config_file():
    """
    TODO DOCUMENTATION
    :return:
    """
    check_file(config_file)
    return read_json(config_file)


# GETS

# SAVE


def save_response(output_path, files):
    """
    TODO DOCUMENTATION
    :param output_path:
    :param files:
    :return:
    """
    if type(files) is not list:
        files = [files]
    out = []
    for i in files:
        output = os.path.join(output_path, os.path.basename(i))
        shutil.copyfile(i, output)
        out.append(output)

    return out


# CLEAN


def clean_tmp_folder():
    """
    TODO DOCUMENTATION
    :return:
    """
    shutil.rmtree(tmp_folder)

