import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ExperimentGroup(Base):
    __tablename__ = 'original'
    id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column(sa.DateTime)

    def __repr__(self):
        return '<Original %r>' % self.name


class ComparisonGroup(Base, ExperimentGroup):
    __tablename__ = 'sample'

    def __repr__(self):
        return f'<Sample {self.name}>'


class Samples(Base, ComparisonGroup):
    __tablename__ = 'samples'
    sample_id = sa.Column(sa.Integer)

    def __repr__(self):
        return f'<Sample {self.id} - {self.date} - {self.sample_id}>'
