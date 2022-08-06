import time

import pandas as pd
from datetime import datetime, timedelta

from model.model import Collections, Groups
from modules.configuration import Configuration
from adapter.database.database import Database


class ImportCSV:
    def __init__(self) -> None:
        self.config = Configuration()
        self.database: Database = Database(self.config)

        self.csv_file = self.config.get_insert_csv_file_path('csv')

    def insert(self, group_id: int, name: str,
               user_id_column_name: str, date_column_name: str, value_column_name: str, csv_file=None) -> None:
        if csv_file is None:
            csv_file = self.csv_file

        print("loading csv file...")
        start_time: float = time.time()
        data: pd.DataFrame = pd.read_csv(csv_file, chunksize=10000000, iterator=True).get_chunk()
        print(f"...has finished [{timedelta(seconds=(time.time() - start_time))}]")

        print("--------------------------------------------------------------------------------")

        print(f"creating new group {name}")
        self.database.get_or_create(model=Groups, id=group_id, name=name)

        print("--------------------------------------------------------------------------------")

        print(f"inserting data into database")
        start_time = time.time()
        rows: list = []
        for index, (_, row) in enumerate(data.iterrows()):
            rows.append({
                'group_id': group_id,
                'user_id': row[user_id_column_name],
                'date': datetime.strptime(row[date_column_name], '%Y-%m-%d').date(),
                'value': row[value_column_name]
            })

            if index % 1000 == 0 and index != 0:
                print(f"inserted {index} rows")
                self.database.session.bulk_insert_mappings(Collections, rows)
                rows = []

        print(f"{len(rows)} rows are now buffered")

        print("--------------------------------------------------------------------------------")
        print("bulking insert...", end="")
        self.database.session.bulk_insert_mappings(Collections, rows)
        print("done")

        print("--------------------------------------------------------------------------------")

        print("committing...", end="")
        self.database.session.commit()
        print("done")

        print("--------------------------------------------------------------------------------")

        print(f"Inserted {len(data)} rows [{timedelta(seconds=(time.time() - start_time))}]")
        print("I am done")
        self.database.close()
