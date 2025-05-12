from os import path

PATH_CONFIG = "./settings.config"


class Configuration:
    def __init__(self, path_file_config):
        self.configurations = {}
        self.path_file_config = path_file_config

    def load_configurations(self):
        if path.isfile(self.path_file_config):
            with open(self.path_file_config, "r", encoding="utf-8") as file:
                for line in file:
                    selected_line = line.replace("\n", "").split(":")
                    self.configurations[selected_line[0].strip()] = (
                        selected_line[1].strip()
                    )
        else:
            return None

    def add_configuration(self, config, value):
        self.configurations[config] = value
        self.save_configuration_file()

    def create_initial_configuration(self, configurations):
        for configuration, value in configurations.items():
            self.configurations[configuration] = value
        self.save_configuration_file()

    def save_configuration_file(self):
        with open(self.path_file_config, "w", encoding="utf-8") as file:
            for config in self.configurations:
                file.write(f"{config}: {self.configurations[config]}\n")
