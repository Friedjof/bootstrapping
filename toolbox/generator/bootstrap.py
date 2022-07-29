import random
from datetime import datetime

from toolbox.configuration.config import Configuration
from toolbox.database.database import Database

from model.model import CollectedData, Groups


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
            new_sample: Groups = Groups(
                id=sample_id + 3,
                name=f"Sample {sample_id + 1}",
            )
            self.database.add(new_sample)
            self.database.commit()
            for index, data in enumerate(sample):
                print(data)
                new_data_point = CollectedData(
                    date=datetime.strptime(data[3], "%Y-%m-%d %H:%M:%S.%f"),
                    user_id=data[2],
                    value=data[4],
                    group_id=new_sample.id
                )
                self.database.add(new_data_point)
            self.database.commit()
        self.database.close()
