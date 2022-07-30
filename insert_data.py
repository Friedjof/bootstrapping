import random
import pandas as pd
from datetime import datetime

from model.model import Collections
from toolbox.configuration.config import Configuration
from toolbox.database.database import Database


class ImportCSV:
    def __init__(self) -> None:
        self.config = Configuration()
        self.database: Database = Database(self.config)

        self.csv_file = self.config.get_insert_csv_file_path('csv')

    def insert(self, group_id) -> None:
        data: pd.DataFrame = pd.read_csv(self.csv_file)
        print(data)
        for index, row in data.iterrows():
            new_data_point = Collections(
                date=datetime.strptime(row['date'], "%Y-%m-%d").date(),
                user_id=row['user_id'],
                value=row['value'],
                group_id=group_id
            )
            self.database.add(new_data_point)

        self.database.commit()
        self.database.close()

        print("I am done")


if __name__ == '__main__':
    import_csv: ImportCSV = ImportCSV()
    import_csv.insert(group_id=2)
