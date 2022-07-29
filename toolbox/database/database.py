from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from toolbox.configuration.config import Configuration


class Database:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

        self.engine = create_engine(self.configuration.get_database_path(), echo=True)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, obj):
        self.session.add(obj)

    def get_session(self):
        return self.session

    def close_session(self):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()
        self.engine.dispose()

    def __del__(self):
        self.close()
