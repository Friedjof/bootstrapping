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

        self.rows.deserialize(qm.get_result(sql_command))

        return self.rows.serialize()

    def plot_samples(self) -> None:
        """
        Plot samples.
        """
        print(f"dataset size {self.serialized_rows}")

        fig = px.line(self.serialized_rows, x="date", y="value", line_shape='spline')
        fig.show()