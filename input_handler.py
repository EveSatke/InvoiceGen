from models.item import Item
from models.juridical_entity import JuridicalEntity
from models.physical_person import PhysicalPerson
from models.supplier import Supplier
from utils.helpers import get_confirmation, get_float_input, get_number_input, get_text_input, get_vat_code


def get_user_input_supplier():
    name = get_text_input("Enter the name of the supplier: ")
    address = get_text_input("Enter the address of the supplier: ")
    registration_code = get_number_input("Enter the code of the supplier: ")
    vat_code = get_vat_code("Enter the VAT code of the supplier (Leave empty or type 'none' if not a VAT payer): ")
    bank_account = get_text_input("Enter the bank account of the supplier: ")
    bank_name = get_text_input("Enter the bank name of the supplier: ")
    entity = JuridicalEntity(name, address, registration_code, vat_code)
    supplier = Supplier(entity, bank_account, bank_name, id="")
    return supplier

def get_user_input_VAT_bank_info(name, address, registration_code):
    vat_code = get_vat_code("Enter the VAT code of the supplier (Leave empty or type 'none' if not a VAT payer): ")
    bank_account = get_text_input("Enter the bank account of the supplier: ")
    bank_name = get_text_input("Enter the bank name of the supplier: ")
    entity = JuridicalEntity(name, address, registration_code, vat_code)
    supplier = Supplier(entity, bank_account, bank_name, id="")
    return supplier

def get_user_input_juridical_buyer(client_name, client_address, client_code) -> JuridicalEntity:
    client_vat_code = get_vat_code("Enter the VAT code of the client (Leave empty or type 'none' if not a VAT payer): ")
    entity = JuridicalEntity(client_name, client_address, client_code, client_vat_code)
    return entity

def get_user_input_physical_person_buyer() -> PhysicalPerson:
    name = get_text_input("Enter the name of the client: ")
    surname = get_text_input("Enter the surname of the client: ")
    address = get_text_input("Enter the address of the client: ")
    vat_code = get_vat_code("Enter the VAT code of the client (Leave empty or type 'none' if not a VAT payer): ")
    person = PhysicalPerson(name, surname, address, vat_code)
    return person

def get_item_input(supplier: Supplier) -> list[Item]:
    items = []
    while True:
        name = get_text_input("Enter item description: ")
        quantity = get_number_input("Enter item quantity: ")
        price = get_float_input("Enter item price: ")

        # Ask for VAT rate only if the supplier is a VAT payer
        vat_rate = 0.0
        if supplier.entity.vat_payer_code:
            vat_rate = get_float_input("Enter item VAT rate (21, 9, 5, 0): ")

        item = Item(name, quantity, price, vat_rate)
        items.append(item)

        if not get_confirmation("Add another item? (y/n): "):
            break
    return items
