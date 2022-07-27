import os
import configparser


class Configuration:
    def __init__(self, config_file: None = None):
        if config_file is None:
            self.config_file = self.get_config_path()
        else:
            self.config_file = config_file

        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def get_database_path(self):
        return self.config['database']['path']

    @staticmethod
    def get_config_template_path() -> str:
        return "data/config/configuration.ini.template"

    @staticmethod
    def get_config_path() -> str:
        return "data/config/configuration.ini"

    @staticmethod
    def config_file_exists() -> bool:
        return os.path.exists(Configuration.get_config_path())
