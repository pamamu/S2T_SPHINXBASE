import json
import os

import shutil

info_file = 'resources/info.json'
config_file = 'config.json'
tmp_folder = 'resources/tmp'
tmp_main_folder = 'audios'


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

def get_sphinxtrain_folder():
    """
    TODO DOCUMENTATION
    :return:
    """
    return read_info_file()['sphinxtrain_bin']


def get_base_model_path():
    """
    TODO DOCUMENTATION
    :return:
    """
    return read_info_file()['base_model_path']


def get_tmp_main_folder():
    """
    TODO DOCUMENTATION
    :return:
    """
    path = os.path.join(tmp_folder, tmp_main_folder)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_counts_folder():
    """
    TODO DOCUMENTATION
    :return:
    """
    path = os.path.join(get_tmp_main_folder(), 'counts')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# SAVE

def save_new_model(model_path):
    """
    TODO DOCUMENTATION
    :param model_path:
    :return:
    """
    shutil.rmtree(get_base_model_path())
    shutil.copytree(model_path, get_base_model_path())


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


def copy_acoustic_model():
    """
    TODO DOCUMENTATION
    :return:
    """
    destination_path = os.path.join(get_tmp_main_folder(), 'es')
    if os.path.isdir(destination_path):
        shutil.rmtree(destination_path)
    shutil.copytree(get_base_model_path(), destination_path)
    return destination_path


def copy_dict(dict_path):
    """
    TODO DOCUMENTATION
    :param dict_path:
    :return:
    """
    shutil.copy(dict_path, os.path.join(get_tmp_main_folder(), 'es.dic'))


# CLEAN


def clean_tmp_folder():
    """
    TODO DOCUMENTATION
    :return:
    """
    shutil.rmtree(tmp_folder)
    os.mkdir(tmp_folder)
    print("OK")


def process_output(output_folder):
    """
    TODO DOCUMENTATION
    :param model_folder:
    :param output_folder:
    :return:
    """
    destination_path = os.path.join(output_folder, 'es-es_acoustic_model')
    if os.path.isdir(destination_path):
        shutil.rmtree(destination_path)
    shutil.copytree(get_base_model_path(), destination_path)
    return destination_path
