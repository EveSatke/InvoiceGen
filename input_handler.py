from models.item import Item
from models.juridical_entity import JuridicalEntity
from models.supplier import Supplier
from utils.helpers import get_float_input, get_number_input, get_text_input, get_vat_code


def get_user_input_supplier():
    supplier_name = get_text_input("Enter the name of the supplier: ")
    supplier_address = get_text_input("Enter the address of the supplier: ")
    supplier_registration_code = get_number_input("Enter the code of the supplier: ")
    supplier_vat_code = get_vat_code("Enter the VAT code of the supplier (Leave empty or type 'none' if not a VAT payer): ")
    supplier_bank_account = get_text_input("Enter the bank account of the supplier: ")
    supplier_bank_name = get_text_input("Enter the bank name of the supplier: ")
    entity = JuridicalEntity(supplier_name, supplier_registration_code, supplier_address, supplier_vat_code)
    supplier = Supplier(entity, supplier_bank_account, supplier_bank_name)
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
