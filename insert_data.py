import random
import datetime
import pandas as pd

from model.model import Collections
from toolbox.configuration.config import Configuration
from toolbox.database.database import Database


class ImportCSV:
    def __init__(self) -> None:
        self.config = Configuration()
        self.database: Database = Database(self.config)

        self.csv_file = self.config.get_insert_csv_file_path()

    def insert(self) -> None:
        data: pd.DataFrame = pd.read_csv(self.csv_file)


if __name__ == '__main__':
    import_csv: ImportCSV = ImportCSV()
    import_csv.insert()
