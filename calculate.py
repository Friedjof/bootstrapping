import sqlite3

from toolbox.generator.bootstrap import Bootstrap
from toolbox.configuration.config import Configuration
from toolbox.query.query_manager import QueryManager


if __name__ == '__main__':
    # loading configuration
    config: Configuration = Configuration()

    # connecting to database
    connection = sqlite3.connect(config.get_database_file_path())

    # creating query manager
    query_manager: QueryManager = QueryManager(connection, config)
    # creating bootstrap object
    bootstrap: Bootstrap = Bootstrap(config=config)

    # customizable section
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # get the peer group dataset
    # you can set the sql command in the queries.py file
    bootstrap.set_original_data(query_manager.get_result(query_name="peer_group"))

    # generate the bootstrap samples
    # here you can set the number of samples you want to generate
    bootstrap.choice(nr_of_samples=10)
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # save the bootstrap samples
    bootstrap.save_samples()

    print("I am done.")
