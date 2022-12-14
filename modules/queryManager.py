import sqlite3
import configparser

from modules.configuration import Configuration


class QueryManager:
    def __init__(self, configuration: Configuration, connection=None) -> None:
        self.configuration: Configuration = configuration
        if connection is None:
            self.connection: sqlite3.Connection = sqlite3.connect(self.configuration.get_database_file_path())
        else:
            self.connection: sqlite3.Connection = connection

        self.query_parser: configparser.ConfigParser = self.configuration.get_query_parser()

        self.space_name: str = "queries"

    def get_result(self, query_name: str, *args, **kwargs) -> list:
        cursor = self.connection.cursor()
        cursor.execute(self.query_parser[self.space_name][query_name].format(**kwargs), args)
        return cursor.fetchall()

    def get_samples(self) -> list[tuple]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Groups")
        return cursor.fetchall()

    def get_nr_of_collections_per_sample(self, sample_id) -> int:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM Collections WHERE group_id = {sample_id}")
        return cursor.fetchone()[0]

    def delete_samples(self, min_group_id: int, max_group_id: int) -> None:
        self.connection.execute(
            f"DELETE FROM Collections WHERE group_id >= {min_group_id} AND group_id <= {max_group_id}"
        )
        self.connection.execute(
            f"DELETE FROM Groups WHERE id >= {min_group_id} AND id <= {max_group_id}"
        )
        self.connection.commit()

    def delete_sample(self, sample_id: int) -> None:
        self.connection.execute(f"DELETE FROM Collections WHERE group_id = {sample_id}")
        self.connection.execute(f"DELETE FROM Groups WHERE id = {sample_id}")
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
