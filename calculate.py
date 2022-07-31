import sqlite3

from toolbox.generator.bootstrap import Bootstrap
from toolbox.configuration.config import Configuration
from toolbox.query.query_manager import QueryManager


if __name__ == '__main__':
    config: Configuration = Configuration()

    connection = sqlite3.connect(config.get_database_file_path())

    query_manager: QueryManager = QueryManager(connection, config)
    bootstrap: Bootstrap = Bootstrap(config=config)

    bootstrap.org = query_manager.get_result("peer_group")

    bootstrap.choice(nr_of_samples=10)
    bootstrap.save_samples(sample_start_id=1)

    print("I am done.")
