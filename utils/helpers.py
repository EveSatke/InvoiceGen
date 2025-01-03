from colorama import Fore
from constants import INPUT_BETWEEN_VALUES, INPUT_MUST_BE_FLOAT, INPUT_MUST_BE_NUMBER, INPUT_NOT_EMPTY
from models.item import Item


def get_text_input(prompt: str) -> str:
    while True:
        text = input(prompt).strip()
        if not text:
            print(INPUT_NOT_EMPTY)
            continue
        return text
    

def get_number_input(prompt: str) -> int:
    while True:
        try:
            user_input = int(input(prompt).strip())
            return user_input
        except ValueError:
            print(INPUT_MUST_BE_NUMBER)

def get_float_input(prompt: str) -> int:
    while True:
        try:
            user_input = float(input(prompt).strip())
            return user_input
        except ValueError:
            print(INPUT_MUST_BE_FLOAT)

def get_vat_code(prompt: str) -> str:
    while True:
        vat_code = input(prompt).strip()
        if vat_code.lower() == "none" or not vat_code:
            return None
        return vat_code
    
def get_menu_input(prompt: str, min_value: int, max_value: int, allow_exit: bool = False) -> int | str:
    while True:
        user_input = input(prompt).strip()

        if allow_exit and user_input =="q":
            return user_input

        try:
            input_number = int(user_input)
            if min_value <= input_number <= max_value:
                return input_number
            print(INPUT_BETWEEN_VALUES.format(min_value=min_value, max_value=max_value))
        except ValueError:
            print(INPUT_MUST_BE_NUMBER)

def get_confirmation(prompt: str) -> bool:
    while True:
        response = input(f"{Fore.YELLOW}\n{prompt}{Fore.RESET}").strip().lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' or 'n'.")