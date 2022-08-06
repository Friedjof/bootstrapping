import sqlite3

from adapter.generator.bootstrap import Bootstrap
from modules.configuration import Configuration
from modules.queryManager import QueryManager


if __name__ == '__main__':
    # loading configuration
    config: Configuration = Configuration()

    # connecting to database
    connection = sqlite3.connect(config.get_database_file_path())

    # creating query manager
    query_manager: QueryManager = QueryManager(config, connection=connection)
    # creating bootstrap object
    bootstrap: Bootstrap = Bootstrap(config=config)

    # customizable section
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # get the peer group dataset
    # you can set the sql command in the queries.ini file
    bootstrap.set_original_dataset(
        dataset=query_manager.get_result(
            query_name="data_as_bootstrap_sample"
        )
    )

    # generate the bootstrap samples
    # here you can set the number of samples you want to generate
    bootstrap.choice(nr_of_samples=10)

    # use the selected users to generate the bootstrap samples
    bootstrap.join_users()
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # save the bootstrap samples
    bootstrap.save_samples()

    print("I am done.")
