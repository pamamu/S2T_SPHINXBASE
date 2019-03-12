from ContainerHandler import ContainerHandler
import Pyro4
from utils.IO import read_json



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

    def generate_acousticmodel(self, input_json, output_folder):
        info_json = read_json(input_json)
        audio_info_path = info_json['audio_info_path']

        # TODO generar .fileids
        # TODO generar .transcription

        # TODO GET BASE_ACOUSTIC_MODEL (carpeta) + LANGUAGE MODEL (.lm.bin) + DICT (.dict)

        # TODO GENERATE ACOUSTIC FEATURE FILES

        # TODO CONVERT SENDUMP AND MDEF FILES

        # TODO ACCUMULATING OBSERVATION

        # TODO CREATE TRANSFORMATION MLLR

        # TODO RECREAR SENDUMP


        return "OK"


if __name__ == '__main__':
    import os
    os.chdir('/opt/project')
    handler = SPHINXBASEHandler('SPHINXBASE', 'PYRO:MainController@localhost:4040')
    print(handler.run(input_json='resources/input.json', output_folder='/srv/shared_folder'))
