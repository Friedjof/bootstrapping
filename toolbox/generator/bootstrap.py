import random
from datetime import datetime
from scipy.stats import bootstrap

import numpy as np

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
            new_sample: Groups = Groups(
                id=sample_id + 3,
                name=f"Sample {sample_id + 1}",
            )
            self.database.add(new_sample)
            self.database.commit()
            for index, data in enumerate(sample):
                print(data)
                new_data_point = Collections(
                    date=datetime.strptime(data[3], "%Y-%m-%d").date(),
                    user_id=data[2],
                    value=data[4],
                    group_id=new_sample.id
                )
                self.database.add(new_data_point)
            self.database.commit()
        self.database.close()


if __name__ == '__main__':
    data = [7, 9, 10, 10, 12, 14, 15, 16, 16, 17, 19, 20, 21, 21, 23]

    # convert array to sequence
    data = (data,)

    # calculate 95% bootstrapped confidence interval for median
    bootstrap_ci = bootstrap(
        data, np.median,
        confidence_level=0.95,
        random_state=1,
        method='percentile'
    )

    # view 95% boostrapped confidence interval
    print(bootstrap_ci.confidence_interval)
