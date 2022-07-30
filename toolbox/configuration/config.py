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

    def get_query_path(self) -> str:
        return self.config['queries']['path']

    def get_query_parser(self) -> configparser.ConfigParser:
        query_parser: configparser.ConfigParser = configparser.ConfigParser()
        query_parser.read(self.get_query_path())
        return query_parser

    def get_database_path(self) -> str:
        return self.config['database']['running']

    def get_backup_database_file_path(self) -> str:
        return self.config['database']['backup_path']

    def get_database_file_path(self) -> str:
        return self.get_database_path().split('///')[1]

    def database_file_exists(self) -> bool:
        return os.path.exists(self.get_database_file_path())

    def get_insert_csv_file_path(self, file_type: str) -> str:
        return self.config['insert'][file_type]

    @staticmethod
    def get_config_template_path() -> str:
        return "data/config/configuration.ini.template"

    @staticmethod
    def get_config_path() -> str:
        return "data/config/configuration.ini"

    @staticmethod
    def config_file_exists() -> bool:
        return os.path.exists(Configuration.get_config_path())
