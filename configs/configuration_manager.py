from os import path

class Configuration():
    def __init__(self, path_file_config):
        self.configurations = {}
        self.path_file_config = path_file_config
    

    def load_configurations(self):
        configs = {}
        if path.isfile(self.path_file_config):
            with open(self.path_file_config) as file:
                for line in file:
                    line = line.replace('\n','').split(":")
                    self.configurations[line[0].strip()] = line[1].strip()
        else:
            return None


    def add_configuration(self, config, value):
        self.configurations[config] = value
        self.save_configuration_file()


    def save_configuration_file(self):
        with open(self.path_file_config, 'w') as file:
            for config in self.configurations:
                file.write(f"{config}:{self.configurations[config]}\n")
