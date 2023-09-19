import sqlite3

from adapter.generator.bootstrap import Bootstrap
from modules.queryManager import QueryManager
from modules.configuration import Configuration
from modules.commandlineInput import CommandlineInput

from commands.interfaces import Command
from commands.commandManager import CommandManager


class Bootstrapping(Command):
    def __init__(self, cm: CommandManager, configuration: Configuration, **kwargs):
        super().__init__(cm, "bootstrap", "This Command creates an Set of Samples", **kwargs)
        self.cm = cm
        self.configuration = configuration
        self.connection = sqlite3.connect(self.configuration.get_database_file_path())
        self.query_manager: QueryManager = QueryManager(self.configuration, connection=self.connection)
        self.bootstrap: Bootstrap = Bootstrap(config=self.configuration)

    def execute(self, *attributes) -> None:
        sample_id: int = CommandlineInput.int_input(
            "Witch sample do you want to use as test-group? ",
            default=0
        )
        print("Reading the test-group dataset...")
        self.bootstrap.set_original_dataset(
            dataset=self.query_manager.get_result(
                query_name="data_as_bootstrap_sample",
                group_id=sample_id
            )
        )

        nr_of_samples: int = CommandlineInput.int_input(
            "How many samples do you want to generate?", default=100)

        print("Generating the bootstrap samples...")
        self.bootstrap.choice(nr_of_samples=nr_of_samples)
        print("...done.")

        if CommandlineInput.yes_no_input(
                "Do you want to join the users to the bootstrap samples? (y/n)", default="yes"):
            self.bootstrap.join_users()

        # save the bootstrap samples
        saving_the_samples: bool = CommandlineInput.yes_no_input("Do you want to save the samples? (y/n)")
        if saving_the_samples:
            print("Saving the bootstrap samples...")
            self.bootstrap.save_samples()
            print("...done.")
        else:
            print("Samples not saved.")

        print("--------------------------------------------------------------------------------")

    def help(self) -> None:
        print("With this command you can create a set of samples for the bootstrapping.")
        print("You can choose how many samples you want to generate and if the users should be joined to the samples.")

    def __repr__(self):
        return f"<Command: {self.name}>"
