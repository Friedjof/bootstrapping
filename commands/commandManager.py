from commands.interfaces import Command


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
