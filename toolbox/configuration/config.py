import os
import configparser
import shutil


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
        return self.config['database']['backup']

    def get_database_file_path(self) -> str:
        return self.get_database_path().split('///')[1]

    def database_file_exists(self) -> bool:
        return os.path.exists(self.get_database_file_path())

    def get_insert_csv_file_path(self, file_type: str) -> str:
        return self.config['insert'][file_type]

    def get_database_logging(self) -> bool:
        return self.config.getboolean('logging', 'database_logging')

    def database_backup_file_exists(self) -> bool:
        return os.path.exists(self.get_backup_database_file_path())

    @staticmethod
    def reset_configuration_file() -> None:
        """
        Reset the configuration file.
        """
        shutil.copy(Configuration.get_config_template_path(), Configuration.get_config_path())

    @staticmethod
    def get_config_template_path() -> str:
        """
        Get the path to the configuration template.
        :return: configuration template path
        """
        return "data/config/configuration.ini.template"

    @staticmethod
    def get_config_path() -> str:
        """
        Get the path to the configuration file.
        :return: configuration file path
        """
        return "data/config/configuration.ini"

    @staticmethod
    def get_database_directory_path() -> str:
        """
        Get the path to the database directory.
        :return: database directory path
        """
        return "data/database"

    @staticmethod
    def get_data_directory_path() -> str:
        """
        Get the path to the data directory.
        :return: data directory path
        """
        return "data/"

    @staticmethod
    def get_query_file_path() -> str:
        """
        Get the path to the query file.
        :param query_name: name of the query
        :return: query file path
        """
        return "data/config/queries.ini"

    @staticmethod
    def get_query_template_path() -> str:
        """
        Get the path to the query template.
        :return: query template path
        """
        return "data/config/queries.ini.template"

    @staticmethod
    def get_config_directory_path() -> str:
        """
        Get the path to the configuration directory.
        :return: configuration directory path
        """
        return "data/config"

    @staticmethod
    def config_file_exists() -> bool:
        """
        Check if the configuration file exists.
        :return: true if the configuration file exists, false otherwise
        """
        return os.path.exists(Configuration.get_config_path())

    @staticmethod
    def config_template_exists() -> bool:
        """
        Check if the configuration template exists.
        :return: true if the configuration template exists, false otherwise
        """
        return os.path.exists(Configuration.get_config_template_path())

    @staticmethod
    def database_directory_exists() -> bool:
        return os.path.exists(Configuration.get_database_directory_path())

    @staticmethod
    def query_file_exists() -> bool:
        return os.path.exists(Configuration.get_query_file_path())

    @staticmethod
    def query_template_exists() -> bool:
        return os.path.exists(Configuration.get_query_template_path())

    @staticmethod
    def setup_is_valid() -> bool:
        return Configuration.config_file_exists() and Configuration.config_template_exists()

    @staticmethod
    def reset_query_file() -> None:
        shutil.copy(Configuration.get_query_template_path(), Configuration.get_query_file_path())
