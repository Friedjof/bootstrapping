import time
import shutil
import os

from toolbox.database.database import Database
from toolbox.configuration.config import Configuration


class InitializeProject:
    def __init__(self, config: Configuration):
        self.config = config

    @staticmethod
    def create_tables():
        Database.create_tables()


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
        if configuration.database_exists():
            print("database file found...")
            print("do you want to delete the database file?")
            print(">> you will lose all your data if you do so. (y/n)", end=": ")
            if input() == 'y':
                print("deleting database file...", end="")
                os.remove(configuration.get_database_path())
                time.sleep(2)
                print("done")
            else:
                print("deletion canceled")
            print("-----------------------------------------------------")

        if configuration.database_backup_exists() or configuration.database_exists():
            print(f"- Database file status:        {configuration.database_exists()}")
            print(f"- Database backup file status: {configuration.database_backup_exists()}")
            print("do you want to RESTORE or BACKUP your database? (y/n)", end=": ")
            if input() == 'y':
                print("b for backup, r for restore", end=": ")
                answer: str = input()
                if answer == 'b':
                    print("backup database...", end="")
                    if configuration.database_exists():
                        shutil.copy(configuration.get_database_path(), configuration.get_backup_database_path())
                        time.sleep(2)
                        print("done")
                    else:
                        print("database file not found!")
                elif answer == 'r':
                    print("restoring database...", end="")
                    if configuration.database_backup_exists():
                        shutil.copy(configuration.get_backup_database_path(), configuration.get_database_path())
                        time.sleep(2)
                        print("done")
                    else:
                        print("database backup file not found!")
                print("-----------------------------------------------------")

        if not configuration.database_exists():
            print(">> do you want to initialize the database? (y/n)", end=": ")
            if input() == 'y':
                print("initialize database...", end="")
                init: InitializeProject = InitializeProject(config=configuration)
                print("done")
                print("-----------------------------------------------------")
                print("create model schema...", end="")
                init.create_tables()
                print("done")
                print("-----------------------------------------------------")
                print("database initialization finished successfully")
            else:
                print("database initialization canceled")
                print("-----------------------------------------------------")
            print("project initialisation has finished successfully")
            print("*****************************************************")
