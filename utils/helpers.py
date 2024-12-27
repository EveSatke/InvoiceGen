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