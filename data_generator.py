import random
import datetime

from model.model import Collections, Groups
from toolbox.configuration.config import Configuration


class DataGenerator:
    def __init__(self):
        self.config = Configuration()

        # Script setup
        self.user_id_start: int = 10000
        self.start_date = datetime.datetime(1970, 1, 1)
        self.date_steps = datetime.timedelta(days=1)
        self.value_range = [50, 60]
        self.group = Groups.get(id=2)

    def generate_data(self):
        for i in range(40):
            collections: list[Collections] = []
            for u in range(75):
                for d in range(119):
                    date = self.start_date + d * self.date_steps
                    value = random.randint(self.value_range[0], self.value_range[1])
                    collections.append(
                        Collections(
                            user_id=self.user_id_start + u,
                            date=date,
                            value=value,
                            group_id=self.group
                        )
                    )
                print(f"{u*i}/3000")
            Collections.bulk_create(collections)
        print("I am done")


if __name__ == '__main__':
    data_generator = DataGenerator()
    data_generator.generate_data()
