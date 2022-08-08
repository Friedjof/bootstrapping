import os
from abc import ABC
from datetime import datetime, date, timedelta
import shutil
from zipfile import ZipFile

from sqlalchemy import create_engine
from sqlalchemy.future import Engine

from adapter.generator.generate_testdata import Generator
from adapter.inserting.csv import ImportCSV

from modules.configuration import Configuration
from modules.commandlineInput import CommandlineInput
from modules.queryManager import QueryManager

from model.model import Base

from commands.interfaces import Command, AbstractKeyword
from commands.commandManager import CommandManager, InputParser


class HelpCommand(Command):
    def __init__(self, cm: CommandManager):
        super().__init__(cm, "help", "Show help")

    def execute(self, *attributes) -> None:
        if len(attributes) == 0:
            print("--------------------------------------------------------------------------------")
            print("Available commands:")
            for command in self.cm.commands:
                print(f'- {command.name:<20} -> {command.description}')
            print("Type 'help <command>' to get more information about a command.")
            print("--------------------------------------------------------------------------------")
        else:
            command_name: str = attributes[0]
            for command in self.cm.commands:
                if command.name == command_name:
                    command.help()
                    return
            print(f"Command '{command_name}' not found.")


class ExitCommand(Command, ABC):
    def __init__(self, cm: CommandManager, **kwargs):
        super().__init__(cm, "exit", "Exit project shell", **kwargs)

    def help(self) -> None:
        print("this command will exit the project shell.")


class DatabaseCommand(Command):
    def __init__(self, cm: CommandManager, configuration: Configuration):
        self.configuration: Configuration = configuration
        super().__init__(cm, "database", "Database commands")

    def execute(self, *args) -> None:
        if len(args) == 0:
            print("[ERROR] You need to specify a command.")
            self.help()
        else:
            command: InputParser = InputParser(args[0])
            if command == AbstractKeyword.CREATE:
                self.create()
            elif command.name == AbstractKeyword.DELETE:
                self.delete(*args[1:] if len(args) > 1 else [])
            elif command.name == AbstractKeyword.BACKUP:
                self.backup()
            elif command.name == AbstractKeyword.RESTORE:
                self.restore()
            elif command.name == AbstractKeyword.INFO:
                self.info()
            elif command.name == AbstractKeyword.REBUILD:
                self.rebuild()
            else:
                print(f"[ERROR] Command '{command}' not found.")
                self.help()

    def create(self) -> None:
        print("[INFO] Creating database...", end="")
        Base.metadata.create_all(create_engine(self.configuration.get_database_path()))
        print("done.")

    def delete(self, *args) -> None:
        if len(args) == 0:
            print("[INFO] Deleting database...")
            engine: Engine = create_engine(self.configuration.get_database_file_path())
            Base.metadata.drop_all(engine)
            print("[INFO] Database deleted.")
        elif len(args) > 0:
            if args[0] == AbstractKeyword.F or args[0] == AbstractKeyword.FILE:
                if self.configuration.database_file_exists():
                    print("[INFO] Deleting database...")
                    os.remove(self.configuration.get_database_file_path())
                    print("[INFO] Database deleted.")
                    print("[TIPP] You can now create a new database with the command 'database create'.")
                else:
                    print("[ERROR] Database file does not exist.")
                    print("[TIPP] You can create a new database with the command 'database create'.")
            else:
                print("[ERROR] Invalid argument.")
                self.help()

    def backup(self) -> None:
        if self.configuration.database_file_exists():
            print("[INFO] Backing up database...")
            shutil.copy(self.configuration.get_database_file_path(), self.configuration.get_backup_database_file_path())
            print("[INFO] Database backed up.")
        else:
            print("[ERROR] Database file not found.")
            if self.configuration.database_backup_file_exists():
                print("[INFO] You can restore the database by typing 'database restore'.")
            else:
                print("there is also no restore database file.")
                print("[INFO] You can create the database by typing 'database create'.")
        print("--------------------------------------------------------------------------------")

    def restore(self) -> None:
        if self.configuration.database_backup_file_exists():
            print("[INFO] Restoring database...")
            shutil.copy(self.configuration.get_backup_database_file_path(), self.configuration.get_database_file_path())
            print("[INFO] Database restored.")
        else:
            print("[ERROR] Database backup file not found.")
            if self.configuration.database_file_exists():
                print("[INFO] You can backup the database by typing 'database backup'.")
            else:
                print("There is also no database file to restore.")
                print("[INFO] The backup path can be specified in the configuration file.")
                print("[INFO] You also can create the database by typing 'database create'.")
        print("--------------------------------------------------------------------------------")

    def rebuild(self) -> None:
        self.delete(AbstractKeyword.FILE)
        self.create()

    def help(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("Database commands:")
        print("- create: Create the database with the given model")
        print("- backup: Backup the database to the backup path in the configuration file")
        print("- restore: Reload the database from the backup path in the configuration file")
        print("- rebuild: Delete the database and create a new one")
        print("- delete [f or file]: Delete the database.")
        print("  If 'f' or 'file' is specified, the database file will be deleted.")
        print("- info: Show information about the database management in this project.")
        print("--------------------------------------------------------------------------------")
        print(">> Note: all databases will not be versioned.")
        print("--------------------------------------------------------------------------------")

    def info(self) -> None:
        # TODO: implement info about storing the database and other stuff
        print("Not implemented yet.")


class ConfigurationCommand(Command, ABC):
    def __init__(self, cm: CommandManager, configuration: Configuration):
        super().__init__(cm, "configuration", "Configuration commands")
        self.configuration: Configuration = configuration

    def execute(self, *args) -> None:
        if len(args) == 0:
            self.help()
        else:
            command: InputParser = InputParser(args[0])
            if command.name == AbstractKeyword.RESET:
                self.configuration.reset_configuration_file()
                print("Reset configuration file.")
            else:
                print(f"Command '{command.name}' not found.")

    def help(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("Configuration commands:")
        print("- reset: Overwrite configuration file with the template configuration file.")
        print("--------------------------------------------------------------------------------")


class ProjectCommand(Command, ABC):
    def __init__(self, cm: CommandManager, configuration: Configuration):
        super().__init__(cm, "project", "Project commands")
        self.configuration: Configuration = configuration

    def execute(self, *args) -> None:
        if len(args) == 0:
            self.help()
        else:
            command: InputParser = InputParser(args[0])
            if command.name == AbstractKeyword.GUIDE:
                self.start_guide()
            elif command.name == AbstractKeyword.SETUP:
                self.start_setup()
            elif command.name == AbstractKeyword.BACKUP:
                self.backup_dialog(*args[1:] if len(args) > 1 else [])
            elif command.name == AbstractKeyword.RESTORE:
                self.restore_dialog(*args[1:] if len(args) > 1 else [])
            elif command.name == AbstractKeyword.REBUILD:
                self.rebuild_project()
            elif command.name == AbstractKeyword.INFO:
                self.info()
            else:
                print(f"Command '{command.name}' not found.")

    def start_guide(self) -> None:
        # TODO: write the guide
        pass

    def start_setup(self) -> None:
        print("[INFO] Setting up project...")
        # This is the checklist for the setup:
        # TODO: programm a configuration or project validator
        # Database check:
        database_directory_exists: bool = self.configuration.database_directory_exists()
        database_file_exists: bool = self.configuration.database_file_exists()
        database_backup_file_exists: bool = self.configuration.database_backup_file_exists()

        # Configuration check:
        configuration_file_exists: bool = self.configuration.config_file_exists()
        configuration_template_file_exists: bool = self.configuration.config_template_exists()

        # Query check:
        query_file_exists: bool = self.configuration.query_file_exists()
        query_template_file_exists: bool = self.configuration.query_template_exists()

        print("--------------------------------------------------------------------------------")
        print("[INFO] Checking database...")
        if not database_directory_exists:
            print("- Creating database directory...", end="")
            os.mkdir(self.configuration.get_database_directory_path())
            print("done.")
        else:
            print("- Database directory exists.")

        if not database_file_exists:
            print("- Creating database file...", end="")
            Base.metadata.create_all(create_engine(self.configuration.get_database_path()))
            print("done.")
            print("  [TIPP] This can also be done by typing 'database create'.")
        else:
            print("- Database file exists.")

        if not database_backup_file_exists:
            print("- [INFO] There is no database backup in the database directory.")
            print("  [TIPP] To create a backup of the database, type 'database backup'.")
        else:
            print("- [INFO] Database backup file exists.")

        print("--------------------------------------------------------------------------------")
        print("[INFO] Checking configuration...")
        if not configuration_file_exists:
            if not configuration_template_file_exists:
                print("[ERROR] Configuration template file not found.")
                print("The project can not run without a configuration file.")
                print("TIPP:")
                print("1. download the configuration file from the github repository.")
                print("2. move the file into the project directory data/config/.")
                print("3. then run the project setup again.")
            else:
                print("- Creating configuration file...", end="")
                self.configuration.reset_configuration_file()
                print("done.")
                print("  [TIPP] To learn more about the configuration file, type 'help configuration'.")
        else:
            print("- Configuration file exists.")

        print("--------------------------------------------------------------------------------")
        print("[INFO] Checking queries...")
        if not query_file_exists:
            if not query_template_file_exists:
                print("[ERROR] Query template file not found.")
                print("The project can not run without a query file.")
                print("TIPP:")
                print("1. download the query file from the github repository.")
                print("2. move the file into the project directory data/config/.")
                print("3. then run the project setup again.")
            else:
                print("- Creating query file...", end="")
                self.configuration.reset_query_file()
                print("done.")
                print("  [TIPP] To learn more about the query file, type 'help query'.")
        else:
            print("- Query file exists.")

        print("SETUP FINISHED SUCCESSFULLY.")
        print("--------------------------------------------------------------------------------")

    def backup_dialog(self, *args) -> None:
        if len(args) == 0:
            print("[ERROR] No project backup path specified.")
            print("[TIPP] To create a backup of the project, type 'project backup <path>'.")
        else:
            path: str = args[0]

            if os.path.exists(path):
                if os.path.isdir(path):
                    filename: str = f"project-backup_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.zip"
                    self.generate_backup_file(path=os.path.join(path, filename))
                elif os.path.isfile(path):
                    print("[WARNING] The backup file already exists.")
                    print("Would you like to overwrite it? (y/n)", end=" ")
                    if input().lower() == "y":
                        os.remove(path)
                        self.generate_backup_file(path=path)
                        print("[INFO] Backup file overwritten.")
                    else:
                        print("[INFO] Backup file not overwritten.")
            else:
                if os.path.exists(os.path.dirname(path)):
                    if os.path.exists(path=path + ".zip"):
                        print("[WARNING] The backup file already exists.")
                        print("Would you like to overwrite it? (y/n)", end=" ")
                        if input().lower() == "y":
                            os.remove(path + ".zip")
                            self.generate_backup_file(path=path)
                            print("[INFO] Backup file overwritten.")
                        else:
                            print("[INFO] Backup file not overwritten.")
                    else:
                        self.generate_backup_file(path=path)
                else:
                    print("[WARNING] The backup path does not exist.")
                    print("          Please specify a valid path.")

    def generate_backup_file(self, path: str) -> None:
        if os.path.splitext(path)[1] != ".zip":
            path += ".zip"

        print(f"[INFO] Creating backup file {path}...")

        with ZipFile(path, "w") as backup_file:
            for root, dirs, files in os.walk(self.configuration.get_database_directory_path()):
                for file in files:
                    backup_file.write(
                        os.path.join(root, file),
                        os.path.relpath(
                            os.path.join(root, file),
                            self.configuration.get_database_directory_path().split("/")[0]
                        )
                    )
            backup_file.write(os.path.abspath(self.configuration.get_query_path()), "queries.ini")
            backup_file.write(os.path.abspath(self.configuration.get_config_path()), "configuration.ini")

        print(f"[INFO] Backup file {path} created.")
        print(f"[TIPP] To restore the backup, type 'project restore {path}'.")

    def restore_dialog(self, *args) -> None:
        if len(args) == 0:
            print("[ERROR] No project backup path specified.")
            print("[TIPP] To restore a backup of the project, type 'project restore <path>'.")
        else:
            path: str = args[0]

            if os.path.isfile(path):
                self.restore_backup_file(path)
            else:
                print("[WARNING] The backup file does not exist.")
                print("          Please specify a valid path.")

    def restore_backup_file(self, path: str) -> None:
        print(f"[INFO] Restoring backup file {path}...")

        with ZipFile(path, "r") as backup_file:
            for file in backup_file.namelist():
                print(f"[DEBUG] Extracting {file}...")
                if file == 'queries.ini':
                    backup_file.extract(file, self.configuration.get_config_directory_path())
                elif file == 'configuration.ini':
                    backup_file.extract(file, self.configuration.get_config_directory_path())
                else:
                    backup_file.extract(file, self.configuration.get_data_directory_path())

    def rebuild_project(self) -> None:
        # TODO: write the rebuild
        pass

    def help(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("Project commands:")
        print("- guide: Show the guide for this project.")
        print("- setup: With this command you can setup the project.")
        print("- backup [path]: zip all your specific files and put them in the given path.")
        print("- restore [path]: restore the project from the given path.")
        print("- rebuild: Rebuild this project. THIS WILL CLEANUP ALL SPECIFIED FILES!")
        print("- info: Show information about the project structure.")
        print("  You can also read the README.md file for all information.")
        print("--------------------------------------------------------------------------------")
        print(">> Note: all projects will not be versioned.")
        print("--------------------------------------------------------------------------------")


class ProjectInfoDialog:
    def __init__(self, configuration: Configuration) -> None:
        super().__init__(configuration)

    @staticmethod
    def show() -> None:
        print("--------------------------------------------------------------------------------")
        print("Project structure:")
        print("- data:")
        print("  - config:")
        print("    - configuration.ini: The configuration file for the project.")
        print("    - queries.ini: The queries file for the project.")
        print("  - database:")
        print("    - <database name>:")
        print("      - <table name>:")
        print("        - <table name>.csv: The table file.")
        print("--------------------------------------------------------------------------------")


class DeleteCommand(Command):
    def __init__(self, cm: CommandManager, configuration: Configuration) -> None:
        super().__init__(cm, name="delete",
                         description="This command will clean up the project in different ways.")
        self.configuration = configuration
        self.query_manager: QueryManager = QueryManager(configuration)

    def execute(self, *args) -> None:
        if len(args) > 0:
            command: InputParser = InputParser(args[0])
            if command.get_command() == AbstractKeyword.SAMPLES:
                self.delete_samples()
            else:
                print(f"[ERROR] Attribute {command.get_command()} not found.")
            print("--------------------------------------------------------------------------------")
        else:
            self.help()

    def help(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("clean <attribute>:")
        print("- samples: This command will delete specific samples in the database.")
        print("--------------------------------------------------------------------------------")

    def delete_samples(self):
        self.query_manager: QueryManager = QueryManager(self.configuration)
        print("[INFO] with this command you can delete specific samples in the database.")
        print("[INFO] Following samples are available:")
        print("--------------------------------------------------------------------------------")
        samples: list[str] = self.query_manager.get_samples()
        for sample in samples:
            print(f"- {sample[0]} > {sample[1]}")
        print("--------------------------------------------------------------------------------")

        delete_multiple: bool = CommandlineInput.yes_no_input("Do you want to delete multiple samples? (y/n)")
        if delete_multiple:
            min_group_id: int = CommandlineInput.int_input("Please enter the minimum sample id:")
            max_group_id: int = CommandlineInput.int_input("Please enter the maximum sample id:")
            print("--------------------------------------------------------------------------------")
            print(f"[INFO] Minimum group id: {min_group_id}")
            print(f"[INFO] Maximum group id: {max_group_id}")
            delete_samples: bool = CommandlineInput.bool_input("Do you want to delete this samples? (y/n)")
            print("--------------------------------------------------------------------------------")
            if delete_samples:
                self.query_manager.delete_samples(min_group_id, max_group_id)
                print("[INFO] Samples deleted.")
            else:
                print("[INFO] Samples not deleted.")
        else:
            sample_id: int = CommandlineInput.int_input("Please enter the sample id:")
            print("--------------------------------------------------------------------------------")
            print(f"[INFO] Sample id: {sample_id}")
            delete_samples: bool = CommandlineInput.yes_no_input("Do you want to delete this samples? (y/n)")
            print("--------------------------------------------------------------------------------")
            if delete_samples:
                self.query_manager.delete_sample(sample_id)
                print("[INFO] Sample deleted.")
            else:
                print("[INFO] Sample not deleted.")

        self.query_manager.close()


class InsertDataCommand(Command):
    def __init__(self, cm: CommandManager, configuration: Configuration) -> None:
        super().__init__(cm, name="insert",
                         description="This command will insert data into the database.")
        self.configuration = configuration
        self.query_manager: QueryManager = QueryManager(configuration)

    def execute(self, *args) -> None:
        if len(args) > 0:
            command: InputParser = InputParser(args[0])
            if command.get_command() == AbstractKeyword.CSV:
                self.insert_samples()
            else:
                print(f"[ERROR] Attribute {command.get_command()} not found.")
            print("--------------------------------------------------------------------------------")
        else:
            self.help()

    def help(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("insert <attribute>:")
        print("- csv: This command will insert data from csv into the database.")
        print("--------------------------------------------------------------------------------")

    def insert_samples(self) -> None:
        import_csv: ImportCSV = ImportCSV()

        print("--------------------------------------------------------------------------------")
        group_id: int = CommandlineInput.int_input("Please enter the sample id:")
        group_name: str = CommandlineInput.string_input("Please enter the sample name:")
        print("--------------------------------------------------------------------------------")

        print("CSV column mapping:")
        user_id_column: str = CommandlineInput.string_input("Name of the user id column in CSV File:")
        date_column_name: str = CommandlineInput.string_input("Name of the date column in CSV File:")
        value_column_name: str = CommandlineInput.string_input("Name of the value column in CSV File:")
        print("--------------------------------------------------------------------------------")

        csv_file_path: str = self.configuration.get_insert_csv_file_path(file_type="csv")
        print(f"[INFO] The CSV file path: {csv_file_path}")
        csv_file_path_correct: bool = CommandlineInput.yes_no_input("Is the CSV file path correct? (y/n)")
        if not csv_file_path_correct:
            csv_file_path = CommandlineInput.special_file_input("Please enter the CSV file path:", "csv")

        import_csv.insert(
            # set id and name of the group which the data should be connected to
            group_id=group_id, name=group_name,

            # set the path to the csv file
            csv_file=csv_file_path,

            # mapping column from csv file to table column
            # write here the column name of the csv file
            user_id_column_name=user_id_column, date_column_name=date_column_name, value_column_name=value_column_name
        )


class GenerateDataCommand(Command):
    def __init__(self, cm: CommandManager, configuration: Configuration) -> None:
        super().__init__(cm, name="generate",
                         description="This command will generate data in the database.")
        self.configuration = configuration
        self.query_manager: QueryManager = QueryManager(configuration)

    def execute(self, *args) -> None:
        if len(args) > 0:
            command: InputParser = InputParser(args[0])
            if command.get_command() == AbstractKeyword.SAMPLE:
                self.generate_samples()
            else:
                print(f"[ERROR] Attribute {command.get_command()} not found.")
            print("--------------------------------------------------------------------------------")
        else:
            self.help()

    def help(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("generate <attribute>:")
        print("- sample: This command will generate a sample and insert it into the database.")
        print("--------------------------------------------------------------------------------")

    def generate_samples(self) -> None:
        start_date: date = CommandlineInput.date_input(
            "Please enter the start date (%Y-%m-%d):", date_format="%Y-%m-%d")
        date_step: timedelta = timedelta(days=CommandlineInput.int_input("Please enter the date step", default=1))
        start_user_id: int = CommandlineInput.int_input("Please enter the start user id", default=1)
        sample_id: int = CommandlineInput.int_input("Please enter the sample id", default=1)
        value_range_min: int = CommandlineInput.int_input("Please enter the minimum value", default=0)
        value_range_max: int = CommandlineInput.int_input("Please enter the maximum value", default=100)
        nr_of_users: int = CommandlineInput.int_input("Please enter the number of users", default=10)
        days_per_user: int = CommandlineInput.int_input("Please enter the number of days per user", default=10)

        print("--------------------------------------------------------------------------------")

        sample_generator: Generator = Generator(
            start_date=start_date, date_steps=date_step,
            start_user_id=start_user_id, group_id=sample_id,
            value_range=(value_range_min, value_range_max)
        )

        if CommandlineInput.yes_no_input("Do you want to generate the data? (y/n)"):
            sample_generator.generate_data(
                users=nr_of_users, days_per_user=days_per_user
            )
            print("[INFO] Data generated.")
        else:
            print("[INFO] Data not generated.")


class ShowCommand(Command):
    def __init__(self, cm: CommandManager, configuration: Configuration) -> None:
        super().__init__(cm, name="show",
                         description="This command will show data from the database.")
        self.configuration = configuration
        self.query_manager: QueryManager = QueryManager(configuration)

    def execute(self, *args) -> None:
        if len(args) > 0:
            command: InputParser = InputParser(args[0])
            if command.get_command() == AbstractKeyword.SAMPLES:
                self.show_samples()
            else:
                print(f"[ERROR] Attribute {command.get_command()} not found.")
        else:
            self.help()

    def help(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("show <attribute>:")
        print("- samples: This command will show all samples from the database.")
        print("--------------------------------------------------------------------------------")

    def show_samples(self) -> None:
        print("+------------------------------------------------------------------------------+")
        print("| Samples                                                                      |")
        print("+------------------------------------------------------------------------------+")
        print("|    ID     |                  Name                    |        Columns        |")
        print("+-----------+------------------------------------------+-----------------------+")
        for sample in self.query_manager.get_samples():
            nr_of_columns: int = self.query_manager.get_nr_of_collections_per_sample(sample[0])
            print(f"| {sample[0]:<9} | {sample[1]:<40} | {nr_of_columns:<21} |")
        print("+-----------+------------------------------------------+-----------------------+")
