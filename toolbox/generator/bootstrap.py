import random
from datetime import datetime

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
        for i in range(nr_of_samples):
            temp_sample: list = []
            for j in range(len(self.org)):
                temp_sample.append(random.choice(self.org))
            self.samples.append(temp_sample)
        return self.samples

    def save_samples(self) -> None:
        for sample_id, sample in enumerate(self.samples):
            new_sample: Groups = Groups.get_or_create(
                id=sample_id + 3,
                name=f"Sample {sample_id + 1}",
            )
            for index, data in enumerate(sample):
                print(f"{type(data)} - {data}")
