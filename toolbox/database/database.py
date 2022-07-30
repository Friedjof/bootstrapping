from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.model import Collections, Groups
from toolbox.configuration.config import Configuration


class Database:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

        self.logging: bool = configuration.get_database_logging()

        self.engine = create_engine(self.configuration.get_database_path(), echo=self.logging)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, obj):
        self.session.add(obj)

    def get_or_create(self, model, **kwargs):
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            self.session.add(instance)
            return instance

    def get_session(self):
        return self.session

    def get_samples(self, **kwargs):
        return self.session.query(Collections).filter_by(**kwargs).all()

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
