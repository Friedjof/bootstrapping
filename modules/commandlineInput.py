class CommandlineInput:
    @staticmethod
    def int_input(prompt: str) -> int:
        while True:
            try:
                return int(input(f"{prompt} "))
            except ValueError:
                print("[ERROR] This is not a valid number.")
                continue

    @staticmethod
    def float_input(prompt: str) -> float:
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("[ERROR] This is not a valid number.")
                continue

    @staticmethod
    def string_input(prompt: str) -> str:
        return input(prompt)

    @staticmethod
    def bool_input(prompt: str) -> bool:
        while True:
            try:
                return bool(input(prompt))
            except ValueError:
                print("[ERROR] This is not a valid boolean.")
                continue

    @staticmethod
    def choice_input(prompt: str, choices: list[str]) -> str:
        while True:
            choice: str = input(prompt)
            if choice in choices:
                return choice
            else:
                print("[ERROR] This is not a valid choice.")
                continue

    @staticmethod
    def int_choice_input(prompt: str, choices: list[int]) -> int:
        while True:
            choice: int = CommandlineInput.int_input(prompt)
            if choice in choices:
                return choice
            else:
                print("[ERROR] This is not a valid choice.")
                continue

    @staticmethod
    def float_choice_input(prompt: str, choices: list[float]) -> float:
        while True:
            choice: float = CommandlineInput.float_input(prompt)
            if choice in choices:
                return choice
            else:
                print("[ERROR] This is not a valid choice.")
                continue

    @staticmethod
    def string_choice_input(prompt: str, choices: list[str]) -> str:
        while True:
            choice: str = CommandlineInput.string_input(prompt)
            if choice in choices:
                return choice
            else:
                print("[ERROR] This is not a valid choice.")
                continue

    @staticmethod
    def yes_no_input(prompt: str, choices: None = None) -> bool:
        if choices is None:
            choices: list[str] = ["yes", "y", "no", "n"]
        while True:
            choice: str = CommandlineInput.string_input(prompt)
            if choice in choices:
                return choice in ["yes", "y"]
            else:
                print("[ERROR] This is not a valid choice.")
                continue
