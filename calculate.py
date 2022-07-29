import sqlite3
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.generator.bootstrap import Bootstrap
from core.configuration.config import Configuration
from core.query.query_manager import QueryManager
from model.model import CollectedData, Groups


if __name__ == '__main__':
    config: Configuration = Configuration()

    connection = sqlite3.connect(config.get_database_file_path())
    query_manager: QueryManager = QueryManager(connection, config)

    engine = create_engine(config.get_database_path(), echo=True)
    session = sessionmaker(bind=engine)()

    data: list = query_manager.get_result("all_data")

    bootstrap: Bootstrap = Bootstrap(org=data)
    samples: list = bootstrap.choice(nr_of_samples=10)

    for sample_id, sample in enumerate(samples):
        new_sample: Groups = Groups(
            id=sample_id + 3,
            name=f"Sample {sample_id + 1}",
        )
        session.add(new_sample)
        session.commit()
        for index, data in enumerate(sample):
            print(data)
            new_data_point = CollectedData(
                date=datetime.datetime.strptime(data[3], "%Y-%m-%d %H:%M:%S.%f"),
                user_id=data[2],
                value=data[4],
                group_id=new_sample.id
            )
            session.add(new_data_point)
        session.commit()
    session.close()

    print("I am done.")
