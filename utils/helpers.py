from colorama import Fore
from constants import INPUT_BETWEEN_VALUES, INPUT_MUST_BE_FLOAT, INPUT_MUST_BE_NUMBER, INPUT_NOT_EMPTY
from models.item import Item
from models.invoice import Invoice
from models.juridical_entity import JuridicalEntity
from models.physical_person import PhysicalPerson
from models.supplier import Supplier


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

def get_float_input(prompt: str) -> float:
    while True:
        try:
            user_input = float(input(prompt).strip())
            return user_input
        except ValueError:
            print(INPUT_MUST_BE_FLOAT)

def get_vat_code(prompt: str) -> str | None:
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

def print_supplier_details(supplier: Supplier):
    print(f"{Fore.YELLOW}Supplier:{Fore.RESET}")
    print(f"{supplier.entity.name}\n{supplier.entity.address}\n{supplier.entity.registration_code}")
    print(f"{supplier.bank_account}\n{supplier.bank_name}")
    if supplier.entity.vat_payer_code:
        print(supplier.entity.vat_payer_code)

def print_buyer_details(buyer: JuridicalEntity | PhysicalPerson):
    print(f"\n{Fore.YELLOW}Buyer:{Fore.RESET}")
    if isinstance(buyer, JuridicalEntity):
        print(f"{buyer.name}\n{buyer.address}\n{buyer.registration_code}")
        if buyer.vat_payer_code:
            print(buyer.vat_payer_code)
    elif isinstance(buyer, PhysicalPerson):
        print(f"{buyer.name} {buyer.surname}\n{buyer.address}")
        if buyer.vat_payer_code:
            print(buyer.vat_payer_code)

def print_items_details(items: list[Item]):
    print(f"\n{Fore.YELLOW}Items:{Fore.RESET}")
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item.name} - {item.quantity} X {item.price} EUR = {item.price * item.quantity} EUR")

def print_invoice_summary(invoice: Invoice):
    print_supplier_details(invoice.supplier)
    print_buyer_details(invoice.buyer)
    print_items_details(invoice.items)
    if invoice.supplier.entity.vat_payer_code:
        print(f"\nTotal VAT: {invoice.total_vat:.2f} EUR")
    print(f"\n{Fore.YELLOW}Total Amount: {invoice.total_amount:.2f} EUR{Fore.RESET}")