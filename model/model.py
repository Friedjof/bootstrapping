import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ExperimentGroup(Base):
    __tablename__ = 'experiment-group'
    id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column(sa.DateTime)

    def __repr__(self):
        return '<ExperimentGroup %r>' % self.name


class ComparisonGroup(Base, ExperimentGroup):
    __tablename__ = 'comparison-group'

    def __repr__(self):
        return f'<ComparisonGroup {self.name}>'


class Samples(Base, ComparisonGroup):
    __tablename__ = 'samples'
    sample_id = sa.Column(sa.Integer)

    def __repr__(self):
        return f'<Samples {self.id} - {self.date} - {self.sample_id}>'
