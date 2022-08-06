from sqlalchemy.orm import sessionmaker

from commands.setup import *
from commands.bootstrap import Bootstrapping


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
        self.command_manager.add_command(
            Bootstrapping(self.command_manager, self.configuration))
        self.command_manager.add_command(
            CleanCommand(self.command_manager, self.configuration))
        self.command_manager.add_command(
            InsertDataCommand(self.command_manager, self.configuration))

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
