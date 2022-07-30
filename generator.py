import random
import datetime

from model.model import Collections
from toolbox.configuration.config import Configuration
from toolbox.database.database import Database


class Generator:
    def __init__(self):
        self.config = Configuration()
        self.database: Database = Database(self.config)

        # Script setup
        self.user_id_start: int = 10000
        self.start_date = datetime.date(1970, 1, 1)
        self.date_steps = datetime.timedelta(days=1)
        self.value_range = [0, 80]
        self.group_id = 2

    def generate_data(self):
        for u in range(10):
            for d in range(1000):
                date = self.start_date + d * self.date_steps
                value = random.randint(self.value_range[0], self.value_range[1])

                cd: Collections = Collections(
                    user_id=self.user_id_start + u,
                    date=date,
                    value=value,
                    group_id=self.group_id
                )

                self.database.add(cd)

            print(f"{u}/10")

        self.database.commit()

        self.database.close()
        print("I am done")


if __name__ == '__main__':
    data_generator = Generator()
    data_generator.generate_data()
