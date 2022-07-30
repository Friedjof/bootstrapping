import pandas as pd
from datetime import datetime

from model.model import Collections, Groups
from toolbox.configuration.config import Configuration
from toolbox.database.database import Database


class ImportCSV:
    def __init__(self) -> None:
        self.config = Configuration()
        self.database: Database = Database(self.config)

        self.csv_file = self.config.get_insert_csv_file_path('csv')

    def insert(self, group_id: int, name: str) -> None:
        data: pd.DataFrame = pd.read_csv(self.csv_file, chunksize=10000000, iterator=True).get_chunk()
        group: Groups = self.database.get_or_create(
            Groups,
            id=group_id, name=name
        )

        for index, row in data.iterrows():
            new_data_point: Collections = self.database.get_or_create(
                model=Collections,
                date=datetime.strptime(row[1], "%Y-%m-%d").date(),
                user_id=row[0],
                value=row[2],
                group_id=group.id
            )
            self.database.add(new_data_point)

        self.database.commit()

        print("I am done")


if __name__ == '__main__':
    import_csv: ImportCSV = ImportCSV()
    import_csv.insert(group_id=2, name="Kontrollgruppe")
