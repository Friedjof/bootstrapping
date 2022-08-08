import pandas as pd
import sqlite3

import plotly.express as px

from adapter.serializer.samples import FinalAggregationSerializer

from modules.queryManager import QueryManager
from modules.configuration import Configuration


class Analyse:
    def __init__(self, configuration: Configuration) -> None:
        self.configuration: Configuration = configuration

        self.rows: FinalAggregationSerializer = FinalAggregationSerializer()
        self.serialized_rows: pd.DataFrame = pd.DataFrame()

    def get_samples(self, sql_command: str) -> pd.DataFrame:
        """
        Get samples from the database.
        """
        connection = sqlite3.connect(self.configuration.get_database_file_path())
        qm: QueryManager = QueryManager(connection=connection, configuration=self.configuration)

        print(qm.get_result(sql_command))

        self.rows.deserialize(qm.get_result(sql_command))

        return self.rows.serialize()

    def plot_samples(self) -> None:
        """
        Plot samples.
        """
        print(f"dataset size {self.serialized_rows}")

        fig = px.line(self.serialized_rows, x="date", y="value", line_shape='spline')
        fig.show()


class CausalImpact:
    def __init__(self, peer_group: pd.DataFrame, samples: list[pd.DataFrame]) -> None:
        self.peer_group: pd.DataFrame = peer_group
        self.samples: list[pd.DataFrame] = samples

    def sample_ranking(self, columns: tuple) -> pd.DataFrame:
        """
        Matching.
        """
        ranking: list[tuple[int, int]] = []

        for sample in self.samples:
            indicator: int = 0
            for r1, r2 in zip(self.peer_group.values, sample.values):
                indicator += abs(r1[1] - r2[1])

            ranking.append((sample.index[0], indicator))

        ranking.sort(key=lambda x: x[1])
        return pd.DataFrame(ranking, columns=columns).set_index(columns[0])
