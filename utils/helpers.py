from colorama import Fore
from models.item import Item


def get_text_input(prompt) -> str:
    while True:
        text = input(prompt).strip().lower()
        if not text:
            print("Input cannot be empty. Please try again.")
            continue
        return text
    

def get_number_input(prompt) -> int:
    while True:
        try:
            user_input = int(input(prompt).strip())
            return user_input
        except ValueError:
            print("Input must be a number. Please try again.")

def get_float_input(prompt) -> int:
    while True:
        try:
            user_input = float(input(prompt).strip())
            return user_input
        except ValueError:
            print("Input must be a float. Please try again.")

def get_vat_code(prompt) -> str:
    while True:
        vat_code = input(prompt).strip()
        if vat_code.lower() == "none" or not vat_code:
            return None
        return vat_code
    
def get_menu_input(prompt, min_value: int, max_value: int, allow_exit: bool = False) -> int:
    while True:
        user_input = input(prompt).strip()

        if allow_exit and user_input =="q":
            return user_input

        try:
            input_number = int(user_input)
            if min_value <= input_number <= max_value:
                return input_number
            print(f"Input must be between {min_value} and {max_value}. Please try again.")
        except ValueError:
            print("Input must be a number. Please try again.")

def get_confirmation(prompt) -> bool:
    while True:
        response = input(f"{Fore.YELLOW}{prompt}{Fore.RESET}").strip().lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' or 'n'.")