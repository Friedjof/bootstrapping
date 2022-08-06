import os


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
    def yes_no_input(prompt: str, choices=None) -> bool:
        if choices is None:
            choices: list[str] = ["yes", "y", "no", "n"]
        while True:
            choice: str = CommandlineInput.string_input(prompt)
            if choice in choices:
                return choice in ["yes", "y"]
            else:
                print("[ERROR] This is not a valid choice.")
                continue

    @staticmethod
    def path_input(prompt: str) -> str:
        while True:
            path: str = CommandlineInput.string_input(prompt)
            if os.path.exists(path):
                return path
            else:
                print("[ERROR] This path does not exist.")
                continue

    @staticmethod
    def file_input(prompt: str) -> str:
        while True:
            file: str = CommandlineInput.string_input(prompt)
            if os.path.isfile(file):
                return file
            else:
                print("[ERROR] This file does not exist.")
                continue

    @staticmethod
    def directory_input(prompt: str) -> str:
        while True:
            directory: str = CommandlineInput.string_input(prompt)
            if os.path.isdir(directory):
                return directory
            else:
                print("[ERROR] This directory does not exist.")
                continue

    @staticmethod
    def special_file_input(prompt: str, file_type: str) -> str:
        print(f"[INFO] The file must exist and have the extension .{file_type}.")
        while True:
            path: str = CommandlineInput.file_input(prompt)
            if os.path.splitext(path)[1].upper() == f".{file_type}".upper():
                return path
            else:
                print("[ERROR] This is not a valid CSV file.")
                continue
