import random
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.model import CollectedData
from core.configuration.config import Configuration


class DataGenerator:
    def __init__(self):
        self.config = Configuration()
        self.engine = create_engine(self.config.get_database_path(), echo=True)
        self.session = sessionmaker(bind=self.engine)()

        # Script setup
        self.user_id_start: int = 10000
        self.start_date = datetime.datetime(1970, 1, 1)
        self.date_steps = datetime.timedelta(days=1)
        self.value_range = [50, 60]
        self.group_id = 2

    def generate_data(self):
        for u in range(10):
            for d in range(10):
                date = self.start_date + d * self.date_steps
                value = random.randint(self.value_range[0], self.value_range[1])

                cd: CollectedData = CollectedData(
                    user_id=self.user_id_start + u,
                    date=date,
                    value=value,
                    group_id=self.group_id
                )

                self.session.add(cd)

            print(f"{u}/10")

        self.session.commit()

        self.session.close()
        print("I am done")


if __name__ == '__main__':
    data_generator = DataGenerator()
    data_generator.generate_data()
