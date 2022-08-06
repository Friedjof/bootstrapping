class AbstractKeyword:
    CSV: str = "csv"
    SAMPLES: str = "samples"
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
