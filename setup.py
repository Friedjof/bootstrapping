import time
import shutil
import os
from abc import ABC

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
        print("--------------------------------------------------------------------------------")
        print("Database commands:")
        print("- create: Create database")
        print("- drop: Drop database")
        print("--------------------------------------------------------------------------------")
        rebuild_configuration_file_dialog()
        self.cm.run_command(InputParser(input(), self.cm.commands))

    def help(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("Database commands:")
        print("- create: Create database")
        print("- drop: Drop database")
        print("- backup: Backup database")
        print("- reload: Reload database")
        print("--------------------------------------------------------------------------------")


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


class BackupCommand(Command):
    def __init__(self, cm: CommandManager, configuration: Configuration):
        self.configuration: Configuration = configuration
        super().__init__(cm, "backup", "Backup all your data from this project in a zip file")

    def execute(self, *args) -> None:
        if len(args) == 0:
            self.help()
        else:
            command: InputParser = InputParser(args[0])
            if command.name == AbstractKeyword.CREATE:
                if len(args) == 1:
                    print("Please specify a path for the backup.")
                else:
                    self.create_backup(path=args[1])
            else:
                print(f"Command '{command.name}' not found.")

    def help(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("The backup command has the following subcommands:")
        print("- create: backups all your data from this project")
        print("--------------------------------------------------------------------------------")

    def create_backup(self, path) -> None:
        # TODO: create backup
        pass


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
            BackupCommand(self.command_manager, self.configuration))

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

    @staticmethod
    def log_database_does_not_exist():
        print("+------------------------------------------------------------------------------+")
        print("| There is no database file. Please create one first.                          |")
        print("| Type 'help create_database' for more information.                            |")
        print("+-------------------------------------------------------------------------------")

    @staticmethod
    def console_read(prompt: str = "$ ") -> str:
        return input(f"[project shell]{prompt}")


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
