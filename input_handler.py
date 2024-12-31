from models.item import Item
from models.juridical_entity import JuridicalEntity
from models.supplier import Supplier
from utils.helpers import get_float_input, get_number_input, get_text_input, get_vat_code


def get_user_input_supplier():
    name = get_text_input("Enter the name of the supplier: ")
    address = get_text_input("Enter the address of the supplier: ")
    registration_code = get_number_input("Enter the code of the supplier: ")
    vat_code = get_vat_code("Enter the VAT code of the supplier (Leave empty or type 'none' if not a VAT payer): ")
    bank_account = get_text_input("Enter the bank account of the supplier: ")
    bank_name = get_text_input("Enter the bank name of the supplier: ")
    entity = JuridicalEntity(name, registration_code, address, vat_code)
    supplier = Supplier(entity, bank_account, bank_name)
    return supplier

def get_user_input_VAT_bank_info(name, address, registration_code):
    vat_code = get_vat_code("Enter the VAT code of the supplier (Leave empty or type 'none' if not a VAT payer): ")
    bank_account = get_text_input("Enter the bank account of the supplier: ")
    bank_name = get_text_input("Enter the bank name of the supplier: ")
    entity = JuridicalEntity(name, address, registration_code, vat_code)
    supplier = Supplier(entity, bank_account, bank_name)
    return supplier

def get_user_input_buyer():
    client_name = get_text_input("Enter the name of the client: ")
    client_code = get_number_input("Enter the code of the client: ")
    client_address = get_text_input("Enter the address of the client: ")
    client_vat_code = get_vat_code("Enter the VAT code of the client (Leave empty or type 'none' if not a VAT payer): ")
    entity = JuridicalEntity(client_name , client_code, client_address, client_vat_code)
    return entity

def get_item_input() -> list[str]:
    items = []
    while True:
        name = input("Enter item name (or 'done' to finish): ").strip()
        if name.lower() == "done":
            break
        
        quantity = get_number_input("Enter item quantity: ")
        price = get_float_input("Enter item price: ")
        
        item = Item(name, quantity, price)
        items.append(item)
    return items
