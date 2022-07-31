import os
from abc import ABC
from datetime import datetime
import shutil
from zipfile import ZipFile

from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker

from model.model import Base
from toolbox.configuration.config import Configuration


class AbstractKeyword:
    CREATE: str = "create"
    INSERT: str = "insert"
    DROP: str = "drop"
    UPDATE: str = "update"
    DELETE: str = "delete"
    RELOAD: str = "reload"
    RESET: str = "reset"
    SHOW: str = "show"
    HELP: str = "help"
    EXIT: str = "exit"
    BACKUP: str = "backup"
    RESTORE: str = "restore"
    INFO: str = "info"
    GUIDE: str = "guide"
    REBUILD: str = "rebuild"
    SETUP: str = "setup"
    F: str = "f"
    FILE: str = "file"


class Command:
    def __init__(self, cm, name: str, description: str, **kwargs):
        self.cm = cm
        self.name: str = name
        self.description: str = description

        # some commands need some attributes
        self.kwargs: dict[str, any] = kwargs

    def execute(self, *attributes) -> None:
        if 'execute' in self.kwargs.keys():
            self.kwargs['execute']()
        else:
            print(f"This command has no execute function: {self.name}")

    def help(self) -> None:
        print(f"This is the description of the command: {self.description}")

    def info(self) -> None:
        print("This function shows more information about the repository.")

    def __repr__(self):
        return f"<Command: {self.name}>"


class InputParser:
    def __init__(self, console_input: str, commands: list[Command] = None) -> None:
        self.name: str = console_input
        self.commands: list[Command] = commands

        self.input_elements: list[str] = self.name.split(" ")

    def get_command(self) -> Command | str | None:
        if self.commands is not None:
            if len(self.input_elements) == 0:
                return None
            command_name: str = self.input_elements[0]
            for command in self.commands:
                if command.name == command_name:
                    return command
        else:
            return self.name

    def __str__(self):
        return f"<InputParser: {self.name}>"


class CommandManager:
    def __init__(self):
        self.commands: list[Command] = []

    def add_command(self, command: Command) -> None:
        self.commands.append(command)

    @staticmethod
    def run_command(parsed_input: InputParser) -> None:
        command: Command = parsed_input.get_command()
        if command is None:
            print("[WARING] This command is undefined. For help type 'help'.")
        else:
            command.execute(*parsed_input.input_elements[1:])


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


class InitializeProject:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.Base = Base

        self.close_commandline: bool = False

        self.engine: Engine = create_engine(self.configuration.get_database_path(), echo=True)
        self.session = sessionmaker(bind=self.engine)()

        # add commands to the command manager
        self.command_manager: CommandManager = CommandManager()
        self.command_manager.add_command(
            HelpCommand(self.command_manager))
        self.command_manager.add_command(
            ExitCommand(self.command_manager, execute=self.exit_commandline))
        self.command_manager.add_command(
            DatabaseCommand(self.command_manager, self.configuration))
        self.command_manager.add_command(
            ConfigurationCommand(self.command_manager, self.configuration))
        self.command_manager.add_command(
            ProjectCommand(self.command_manager, self.configuration))

    def start_console(self):
        self.log_welcome()

        if not self.configuration.database_file_exists():
            self.log_database_does_not_exist()

        while not self.close_commandline:
            user_input: str = self.console_read()
            CommandManager.run_command(
                parsed_input=InputParser(
                    console_input=user_input,
                    commands=self.command_manager.commands
                )
            )

    def migrate_database(self):
        self.Base.metadata.create_all(self.engine)

    def exit_commandline(self):
        print("Exiting...")
        self.close_commandline = True

    @staticmethod
    def log_welcome():
        print("+------------------------------------------------------------------------------+")
        print("| Welcome to the project shell!                                                |")
        print("+------------------------------------------------------------------------------+")
        print("| Type 'exit' to exit the shell.                                               |")
        print("| Type 'help' to get a list of available commands.                             |")
        print("+------------------------------------------------------------------------------+")
        print("| If you are running this project for the FIRST TIME, you should run the       |")
        print("| 'project setup' command to create important files.                           |")
        print("+------------------------------------------------------------------------------+")
        print("| More information can be found in the README.md file or with the command      |")
        print("| 'project guide'.                                                             |")
        print("+------------------------------------------------------------------------------+")

    @staticmethod
    def log_database_does_not_exist():
        print("+------------------------------------------------------------------------------+")
        print("| There is no database file. Please create one first.                          |")
        print("| Type 'help create_database' for more information.                            |")
        print("+-------------------------------------------------------------------------------")

    @staticmethod
    def console_read(prompt: str = "$ ") -> str:
        return input(f"[project shell]{prompt}")


if __name__ == '__main__':
    print("********************************************************************************")
    if not Configuration.setup_is_valid():
        if Configuration.config_template_exists():
            print("[WARNING] Configuration file not found.")
            print("> the setup console is not able to start without a configuration file.")
            print("would you like to create a new configuration file? (y/n)", end=": ")
            if input() == 'y':
                Configuration.reset_configuration_file()
                print("done")
            else:
                print("exit...")
                print("********************************************************************************")
                exit(0)
        else:
            # TODO: Programm a script with loads the newest version of the configuration file from the github repository
            print("[ERROR] Configuration file or configuration template not found.")
            print("> the setup console is not able to start.")
            print("Please create a configuration file or a configuration template and start the setup console again.")
            print("You can get a template configuration file from the github repository.")
            print("exit...")
            print("********************************************************************************")
            exit(0)

    config: Configuration = Configuration()
    initialize_project: InitializeProject = InitializeProject(configuration=config)
    initialize_project.start_console()
