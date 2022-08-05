import sqlite3
import configparser

from modules.config import Configuration


class QueryManager:
    def __init__(self, connection: sqlite3.Connection, configuration: Configuration) -> None:
        self.connection: sqlite3.Connection = connection
        self.configuration: Configuration = configuration

        self.query_parser: configparser.ConfigParser = configuration.get_query_parser()

        self.space_name: str = "queries"

    def get_result(self, query_name: str, *args) -> list:
        cursor = self.connection.cursor()
        cursor.execute(self.query_parser[self.space_name][query_name], args)
        return cursor.fetchall()
