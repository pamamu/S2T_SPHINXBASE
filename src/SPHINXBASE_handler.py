import Pyro4

from ContainerHandler import ContainerHandler
from utils import sphinx_utils
from utils.IO import read_json, copy_acoustic_model, copy_dict, save_new_model, clean_tmp_folder, process_output, \
    check_file


@Pyro4.expose
class SPHINXBASEHandler(ContainerHandler):
    def __init__(self, container_name, main_uri):
        super(SPHINXBASEHandler, self).__init__(container_name, main_uri)

    def run(self, **kwargs):
        if 'input_json' in kwargs and 'output_folder' in kwargs:
            print("Container {}: Runned with {}".format(self.container_name, kwargs))
            self.running = True
            result = self.generate_acousticmodel(kwargs['input_json'], kwargs['output_folder'])
            self.running = False
            return result
        else:
            raise TypeError('input_json and output_folder required')

    def info(self):
        pass

    def reduce_language_model(self, language_model_path, language_model_path_out):
        """
        TODO DOCUMENTATION
        :param language_model_path:
        :param language_model_path_out:
        :return:
        """
        return sphinx_utils.reduce_language_model(language_model_path, language_model_path_out)

    def generate_acousticmodel(self, input_json, output_folder):
        clean_tmp_folder()

        info_json = read_json(input_json)

        audio_info_path = info_json['audio_info_path']
        check_file(audio_info_path)
        language_model_path = info_json['language_model']
        check_file(language_model_path)
        dictionary_path = info_json['dictionary']
        check_file(dictionary_path)

        fileids_path, transcription_path = sphinx_utils.generate_files_structure(read_json(audio_info_path))

        sphinx_utils.convert_lm(language_model_path)

        copy_dict(dictionary_path)

        model_folder = copy_acoustic_model()

        sphinx_utils.generate_aff(model_folder, fileids_path)

        sphinx_utils.convert_mdef(model_folder)

        sphinx_utils.accumulate_obs_count()

        # mllr_matrix = sphinx_utils.mllr_transformation(model_folder)

        sphinx_utils.map_transformation(model_folder)

        save_new_model(model_folder)

        clean_tmp_folder()

        return process_output(output_folder)


if __name__ == '__main__':
    handler = SPHINXBASEHandler('SPHINXBASE', 'PYRO:MainController@localhost:4040')
    print(handler.run(input_json='/srv/shared_folder/input_sphinxbase.json', output_folder='/srv/shared_folder'))
