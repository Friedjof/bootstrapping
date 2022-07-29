import sqlite3

from core.generator.bootstrap import Bootstrap
from core.configuration.config import Configuration
from core.query.query_manager import QueryManager


if __name__ == '__main__':
    config: Configuration = Configuration()

    connection = sqlite3.connect(config.get_database_file_path())
    query_manager: QueryManager = QueryManager(connection, config)

    data: list = query_manager.get_result("distinct_users")

    bootstrap: Bootstrap = Bootstrap(org=data)
    samples: list = bootstrap.choice(nr_of_samples=1)

    for index, sample in enumerate(samples[0]):
        print(index, sample)

