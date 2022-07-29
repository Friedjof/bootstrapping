import time
import shutil

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


def rebuild_configuration_file_dialog():
    if input() == 'y':
        print("creating configuration file...", end="")
        shutil.copy(Configuration.get_config_template_path(), Configuration.get_config_path())
        time.sleep(2)
        print("done")
    else:
        print("rebuild configuration file canceled")
        print("-----------------------------------------------------")


if __name__ == '__main__':
    print("*****************************************************")
    if not Configuration.config_file_exists():
        print("no configuration file found...")
        print("do you want to create the configuration file? (y/n)", end=": ")
        rebuild_configuration_file_dialog()
    else:
        print("do you want to rebuild the configuration file?")
        print(">> you will lose all your settings if you do so. (y/n)", end=": ")
        rebuild_configuration_file_dialog()

    if Configuration.config_file_exists():
        print("read configuration file...", end="")
        configuration: Configuration = Configuration()
        print("done")
        print("-----------------------------------------------------")
        if configuration.database_file_exists():
            print("database file found...")
            print("do you want to delete the database file?")
            print(">> you will lose all your data if you do so. (y/n)", end=": ")
            if input() == 'y':
                print("deleting database file...", end="")
                shutil.rmtree(configuration.get_database_file_path())
                time.sleep(2)
                print("done")
            else:
                print("deletion canceled")
            print("-----------------------------------------------------")

        print("do you want to RESTORE or BACKUP your database? (y/n)", end=": ")
        if input() == 'y':
            print("b for backup, r for restore", end=": ")
            answer: str = input()
            if answer == 'b':
                print("backup database...", end="")
                shutil.copy(configuration.get_database_file_path(), configuration.get_backup_database_file_path())
                time.sleep(2)
                print("done")
            elif answer == 'r':
                print("restoring database...", end="")
                shutil.copy(configuration.get_backup_database_file_path(), configuration.get_database_file_path())
                time.sleep(2)
                print("done")

        print(">> do you want to initialize the database? (y/n)", end=": ")
        if input() == 'y':
            print("initialize database...", end="")
            init: InitializeProject = InitializeProject(config=configuration)
            print("done")
            print("-----------------------------------------------------")
            print("create model schema...")
            init.migrate_database()
            print("...done")
            print("-----------------------------------------------------")
            print("database initialization finished successfully")
        else:
            print("database initialization canceled")
            print("-----------------------------------------------------")
        print("project initialisation has finished successfully")
        print("*****************************************************")
