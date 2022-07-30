import pandas as pd
import sqlite3

import plotly.express as px
from causalimpact import CausalImpact

from toolbox.serializer.samples import FinalAggregationSerializer
from toolbox.query.query_manager import QueryManager
from toolbox.configuration.config import Configuration


class Analyse:
    def __init__(self, configuration: Configuration) -> None:
        self.configuration: Configuration = configuration

        self.rows: FinalAggregationSerializer = FinalAggregationSerializer()
        self.serialized_rows: pd.DataFrame = self.get_samples()

    def get_samples(self) -> pd.DataFrame:
        """
        Get samples from the database.
        """
        connection = sqlite3.connect(self.configuration.get_database_file_path())
        qm: QueryManager = QueryManager(connection=connection, configuration=self.configuration)

        self.rows.deserialize(qm.get_result("final_aggregation"))

        return self.rows.serialize()

    def plot_samples(self) -> None:
        """
        Plot samples.
        """
        print(f"dataset size {self.serialized_rows}")

        fig = px.line(self.serialized_rows, x="date", y="value", line_shape='spline')
        fig.show()


if __name__ == '__main__':
    analysis: Analyse = Analyse(configuration=Configuration())
    analysis.get_samples()

    print(analysis.serialized_rows)

    ci = CausalImpact(analysis.serialized_rows, [0, 4], [5, 10])
    print(ci.summary())
    print(ci.summary(output='report'))
    ci.plot()
