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

    def set_original_data(self, org: list) -> None:
        self.org = org

    def choice(self, nr_of_samples: int, output_size: int = None) -> list:
        """
        Bootstrapping
        """
        if output_size is None:
            output_size = len(self.org)

        start_time: float = time.time()
        for i in range(nr_of_samples):
            temp_sample: list = []
            for j in range(output_size):
                temp_sample.append(random.choice(self.org))
            self.samples.append(temp_sample)
            print(f"created {i + 1}/{nr_of_samples} samples in {timedelta(seconds=(time.time() - start_time))}")
        print(f"inserted {nr_of_samples} samples in {timedelta(seconds=(time.time() - start_time))}")
        return self.samples

    def save_samples(self, sample_start_id: int = None) -> None:
        if sample_start_id is None:
            sample_start_id = self.database.get_max_group_id() + 1

        total_time_start: float = time.time()
        for sample_id, sample in enumerate(self.samples):
            new_sample: Groups = Groups(
                id=sample_id + sample_start_id,
                name=f"Sample {sample_id + 1}",
            )
            self.database.get_or_create(model=Groups, id=new_sample.id, name=new_sample.name)
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
        print(f"inserted {len(self.samples)} samples in {timedelta(seconds=(time.time() - total_time_start))}")
        self.database.close()
