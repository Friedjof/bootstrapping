import datetime as dt

import numpy as np
import pandas as pd


class CollectionRow:
    def __init__(self, row: tuple[int, int, dt.date, int]):
        self.id: int = row[0]
        self.sample_id: int = row[1]
        self.date: dt.date = row[2]
        self.value: int = row[3]

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "sample_id": self.sample_id,
            "date": self.date,
            "value": self.value
        }


class CollectionSerializer:
    dataset: np.ndarray

    def deserialize(self, rows: list[tuple[int, int, dt.date, int]]) -> None:
        self.dataset = np.array([CollectionRow(row) for row in rows])

    def serialize(self) -> pd.DataFrame:
        return pd.DataFrame(
            [row.serialize() for row in self.dataset],
            columns=['id', 'sample_id', 'date', 'value']
        ).set_index('id')
