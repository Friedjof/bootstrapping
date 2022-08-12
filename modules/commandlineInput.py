import os
import datetime


class CommandlineInput:
    @staticmethod
    def int_input(prompt: str, default: int = 0) -> int:
        while True:
            user_input: str = input(f"{prompt} [default={default}] ")
            if user_input.isdigit():
                return int(user_input)
            elif user_input == '':
                return default
            else:
                print("[ERROR] This is not a valid number.")
                continue

    @staticmethod
    def float_input(prompt: str, default: float = 0.0) -> float:
        while True:
            try:
                return float(input(f"{prompt} [default={default}] "))
            except ValueError:
                print("[ERROR] This is not a valid number.")
                continue

    @staticmethod
    def string_input(prompt: str) -> str:
        return input(prompt)

    @staticmethod
    def bool_input(prompt: str, default: bool = False) -> bool:
        while True:
            try:
                return bool(input(f"{prompt} [default={default}] "))
            except ValueError:
                print("[ERROR] This is not a valid boolean.")
                continue

    @staticmethod
    def int_choice_input(prompt: str, choices: list[int]) -> int:
        for choice in choices:
            print(f"{choices.index(choice)}: {choice}")
        while True:
            choice: int = CommandlineInput.int_input(f"{prompt} ")
            if choice in choices:
                return choice
            else:
                print("[ERROR] This is not a valid choice.")
                continue

    @staticmethod
    def float_choice_input(prompt: str, choices: list[float]) -> float:
        for choice in choices:
            print(f"{choices.index(choice)}: {choice}")
        while True:
            choice: float = CommandlineInput.float_input(prompt)
            if choice in choices:
                return choice
            else:
                print("[ERROR] This is not a valid choice.")
                continue

    @staticmethod
    def string_choice_input(prompt: str, choices: list[str]) -> str:
        for choice in choices:
            print(f"{choices.index(choice)}: {choice}")
        while True:
            choice: str = CommandlineInput.string_input(prompt)
            if choice in choices:
                return choice
            else:
                print("[ERROR] This is not a valid choice.")
                continue

    @staticmethod
    def yes_no_input(prompt: str, choices=None, default: str = "no") -> bool:
        if choices is None:
            choices: list[str] = ["yes", "y", "no", "n"]
        while True:
            choice: str = CommandlineInput.string_input(f"{prompt} [default={default}] ")
            if choice in choices:
                return choice in ["yes", "y"]
            else:
                if choice == "":
                    return default in ["yes", "y"]
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

    @staticmethod
    def date_input(param, date_format: str = "%Y-%m-%d") -> datetime.date:
        while True:
            try:
                return datetime.datetime.strptime(cls.string_input(param), date_format).date()
            except ValueError:
                print("[ERROR] This is not a valid date.")
                continue

    @staticmethod
    def time_input(param, date_format: str = "%H:%M:%S") -> datetime.time:
        while True:
            try:
                return datetime.datetime.strptime(CommandlineInput.string_input(param), date_format).time()
            except ValueError:
                print("[ERROR] This is not a valid time.")
                continue

    @staticmethod
    def date_time_input(param, date_format: str = "%Y-%m-%d %H:%M:%S") -> datetime.datetime:
        while True:
            try:
                return datetime.datetime.strptime(CommandlineInput.string_input(param), date_format)
            except ValueError:
                print("[ERROR] This is not a valid date and time.")
                continue

    @staticmethod
    def date_time_choice_input(param, date_format: str = "%Y-%m-%d %H:%M:%S", choices: list[datetime.datetime] = None) -> datetime.datetime:
        if choices is None:
            choices = []
        for choice in choices:
            print(f"{choices.index(choice)}: {choice.strftime(date_format)}")
        while True:
            choice: datetime.datetime = CommandlineInput.date_time_input(param, date_format)
            if choice in choices:
                return choice
            else:
                print("[ERROR] This is not a valid choice.")
                continue
