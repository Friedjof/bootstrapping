import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)

    def __repr__(self):
        return f'<Groups(name={self.name}, description={self.description})>'


class Collections(Base):
    """
    You may have to change this table if this table is not
    in the same format as the data you want to store.
    """
    __tablename__ = 'collections'
    id = sa.Column(sa.Integer, primary_key=True)
    group_id = sa.Column(sa.ForeignKey('groups.id'))

    # here you can change the table format
    user_id = sa.Column(sa.Integer)
    date = sa.Column(sa.Date)
    value = sa.Column(sa.Integer)

    def __repr__(self):
        return f'<CollectedData {", ".join([f"{v}" for v in self.__dict__.vales()])}>'
