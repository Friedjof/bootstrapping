import random
import time
from datetime import datetime, timedelta

from toolbox.configuration.config import Configuration
from toolbox.database.database import Database

from model.model import Collections, Groups


class Bootstrap:
    def __init__(self, config, org: list | None = None) -> None:
        if org is None:
            self.org: list = []
        else:
            self.org: list = org

        self.config: Configuration = config

        self.samples: list = []

        self.database: Database = Database(self.config)

    def choice(self, nr_of_samples: int) -> list:
        """
        Bootstrapping
        """
        start_time: float = time.time()
        for i in range(nr_of_samples):
            temp_sample: list = []
            for j in range(len(self.org)):
                temp_sample.append(random.choice(self.org))
            self.samples.append(temp_sample)
            print(f"{i + 1}/{nr_of_samples}")
        print(f"inserted {nr_of_samples} samples in {timedelta(seconds=(time.time() - start_time))}")
        return self.samples

    def save_samples(self) -> None:
        for sample_id, sample in enumerate(self.samples):
            new_sample: Groups = Groups(
                id=sample_id + 3,
                name=f"Sample {sample_id + 1}",
            )
            self.database.add(new_sample)
            self.database.commit()
            start_time: float = time.time()
            rows: list[dict] = []
            for index, data in enumerate(sample):
                rows.append({
                    'group_id': new_sample.id,
                    'user_id': data[2],
                    'date': datetime.strptime(data[3], "%Y-%m-%d").date(),
                    'value': data[4]
                })
                if index % 10000 == 0 and index != 0:
                    print(f"inserted {index} rows")
            self.database.session.bulk_insert_mappings(Collections, rows)
            self.database.commit()
            print(f"inserted {len(rows)} rows in {timedelta(seconds=(time.time() - start_time))}")
        self.database.close()
