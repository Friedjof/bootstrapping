import datetime as dt
import numpy as np
import pandas as pd


class FinalAggregationRow:
    date: dt.date
    sample_id: int
    value: int
    index: int

    # Date format for incoming data and outgoing data
    incoming_date_format: str = "%Y-%m-%d"
    outgoing_date_format: str = "%d.%m.%Y"

    def __init__(self, index: int):
        self.index: int = index

    def deserialize(self, row: list[str, int, int]):
        self.date = dt.datetime.strptime(row[0], self.incoming_date_format).date()
        self.sample_id = int(row[1])
        self.value = int(row[2])
        return self

    def serialize(self) -> dict:
        return {
            'sample_id': self.sample_id,
            "date": self.date.strftime(self.outgoing_date_format),
            "value": self.value
        }

    def serialize_date(self) -> str:
        return self.date.strftime(self.outgoing_date_format)

    def __repr__(self) -> str:
        return f'<FinalAggregationRow(date={self.serialize_date()}, sample_id={self.sample_id}, value={self.value})>'


class FinalAggregationSerializer:
    dataset: np.ndarray

    def deserialize(self, rows: list[list[str, int, int]]) -> any:
        self.dataset = np.array([FinalAggregationRow(index).deserialize(row) for index, row in enumerate(rows)])
        return self

    def serialize(self, columns: tuple = None, **kwargs) -> pd.DataFrame:
        if columns is None:
            columns: tuple[str, str] = ('x', 'y')
        return pd.DataFrame([row.serialize() for row in self.dataset], columns=columns, **kwargs).set_index(columns[0])
