from model.model import Collections, Groups
from toolbox.configuration.config import Configuration


class Database:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    @staticmethod
    def create_tables():
        Collections.create_table()
        Groups.create_table()
