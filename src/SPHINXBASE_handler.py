from ContainerHandler import ContainerHandler
import Pyro4


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
        # TODO IMPLEMENT acoustic model generation
        return "OK"
