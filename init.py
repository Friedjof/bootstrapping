import os
import time

from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker

from model.model import Base
from core.configuration.config import Configuration


class InitializeProject:
    def __init__(self, config: Configuration):
        self.config = config
        self.Base = Base

        self.engine: Engine = create_engine(self.config.get_database_path(), echo=True)
        self.session = sessionmaker(bind=self.engine)()

    def migrate_database(self):
        self.Base.metadata.create_all(self.engine)


if __name__ == '__main__':
    print("*****************************************************")
    if not Configuration.config_file_exists():
        print("no configuration file found...")
        print("do you want to create the configuration file? (y/n)", end=": ")
        if input() == 'y':
            print("-----------------------------------------------------")
            print("creating configuration file...", end="")
            os.popen(f'cp {Configuration.get_config_template_path()} {Configuration.get_config_path()}')
            time.sleep(2)
            print("done")
        else:
            print("-----------------------------------------------------")
            print("initialization canceled")

    if Configuration.config_file_exists():
        print("read configuration file...", end="")
        configuration: Configuration = Configuration()
        print("done")
        print("-----------------------------------------------------")
        print("initialize database...", end="")
        init: InitializeProject = InitializeProject(config=configuration)
        print("done")
        print("-----------------------------------------------------")
        print("create model schema...")
        init.migrate_database()
        print("...done")
        print("-----------------------------------------------------")
        print("initialization finished successfully")
        print("*****************************************************")
