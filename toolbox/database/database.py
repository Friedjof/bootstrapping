from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from model.model import Collections, Groups
from toolbox.configuration.config import Configuration


class Database:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

        self.logging: bool = configuration.get_database_logging()

        self.engine = create_engine(self.configuration.get_database_path(), echo=self.logging)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, obj) -> None:
        self.session.add(obj)

    def insert_rows(self, model: object, rows: list[dict]) -> None:
        self.session.bulk_insert_mappings(model, rows)

    def get_or_create(self, model, **kwargs) -> object:
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            self.session.add(instance)
            return instance

    def get_session(self) -> sessionmaker:
        return self.session

    def get_samples(self, **kwargs) -> list:
        return self.session.query(Collections).filter_by(**kwargs).all()

    def get_max_group_id(self) -> int:
        return self.session.query(func.max(Groups.id)).scalar() or 0

    def close_session(self) -> None:
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()
        self.engine.dispose()
