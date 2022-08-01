import random
import datetime
import time

from toolbox.configuration.config import Configuration
from toolbox.database.database import Database
from model.model import Collections


class Generator:
    def __init__(
            self,
            start_date: datetime.date = datetime.date(1970, 1, 1),
            date_steps: datetime.timedelta = datetime.timedelta(days=1),
            start_user_id: int = 1, group_id: int = 1, value_range: tuple = (0, 100)
    ):
        self.config = Configuration()
        self.database: Database = Database(self.config)

        self.user_id_start: int = start_user_id
        self.start_date: datetime.date = start_date
        self.date_steps: datetime.timedelta = date_steps
        self.value_range = value_range
        self.group_id = group_id

    def generate_data(self, users: int = 100, days_per_user: int = 100):
        total_start_time = time.time()
        for u in range(users):
            start_time = time.time()
            rows: list[dict] = []
            for d in range(days_per_user):
                date = self.start_date + d * self.date_steps
                value = random.randint(self.value_range[0], self.value_range[1])

                rows.append(dict(
                    user_id=self.user_id_start + u,
                    date=date,
                    value=value,
                    group_id=self.group_id
                ))

            self.database.insert_rows(Collections, rows)
            print(f"inserted {u + 1}/{users} users in {datetime.timedelta(seconds=(time.time() - start_time))}")

        self.database.commit()
        print(f"Total time: {time.time() - total_start_time}")

        self.database.close()
        print("I am done")
