from peewee import *
from toolbox.configuration.config import Configuration


db = SqliteDatabase(Configuration().get_database_path())


class BaseModel(Model):
    class Meta:
        database = db


class Groups(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(null=False)

    def __repr__(self):
        return f'<Groups(name={self.name}, description={self.description})>'


class Collections(BaseModel):
    """
    You may have to change this table if this table is not
    in the same format as the data you want to store.
    """
    id = PrimaryKeyField(null=False)
    group_id = ForeignKeyField(Groups, null=False)

    # here you can change the table format
    user_id = IntegerField(null=False)
    date = DateField(null=False)
    value = IntegerField(null=False)

    def __repr__(self):
        return f'<CollectedData {", ".join([f"{v}" for v in self.__dict__.vales()])}>'
