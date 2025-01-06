from enum import Enum
from colorama import Fore
import logging
from company_searcher import CompanySearcher
from constants import CREATE_SUPPLIER_HEADER, DELETE_SUPPLIER_HEADER, INPUT_BETWEEN_VALUES, MENU_PROMPT, INPUT_MUST_BE_NUMBER, MENU_PROMPT_WITH_EXIT, SEARCH_RESULTS_HEADER, SEARCH_SUPPLIER_HEADER, SELECT_SUPPLIER_HEADER, SUPPLIER_ADDITIONAL_INFO, SUPPLIER_CREATED_MESSAGE, SUPPLIER_DELETED_MESSAGE, SUPPLIER_LIST_HEADER, SUPPLIER_NOT_DELETED_MESSAGE, SUPPLIER_NOT_SAVED_MESSAGE, UNEXPECTED_ERROR, SUPPLIER_MANAGER_HEADER, DIVIDER
from csv_reader import CsvReader
from input_handler import get_user_input_VAT_bank_info, get_user_input_supplier
from json_handler import JsonHandler
from models.juridical_entity import JuridicalEntity
from models.supplier import Supplier
from utils.helpers import get_confirmation, get_menu_input, get_text_input


class SubMenuOption(Enum):
    SEARCH_ADD_SUPPLIER = "Search and create supplier"
    ADD_MANUALLY_SUPPLIER = "Enter supplier details manually"
    VIEW_SUPPLIERS = "View all suppliers"
    DELETE_SUPPLIER = "Delete a supplier"
    EXIT = "Return to main menu"

class SupplierManager:
    FILE_PATH = "data/suppliers.json"

    def __init__(self, json_handler: JsonHandler, csv_reader: CsvReader, company_searcher: CompanySearcher):
        self.json_handler = json_handler
        self.csv_reader = csv_reader
        self.company_searcher = company_searcher
        self.suppliers = self._load_suppliers_from_json()
        self.sub_menu_options = {
            SubMenuOption.SEARCH_ADD_SUPPLIER: self._handle_search_add_supplier,
            SubMenuOption.ADD_MANUALLY_SUPPLIER: self._handle_add_supplier,
            SubMenuOption.VIEW_SUPPLIERS: self._handle_view_suppliers,
            SubMenuOption.DELETE_SUPPLIER: self._handle_delete_supplier,
            SubMenuOption.EXIT: self._handle_return
        }

    def _load_suppliers_from_json(self) -> list[Supplier]:
        supplier_data = self.json_handler.load_json(SupplierManager.FILE_PATH)
        suppliers = []
        for data in supplier_data:
            entity_data = data['entity']
            entity = JuridicalEntity(
                name=entity_data['name'],
                address=entity_data['address'],
                registration_code=entity_data['registration_code'],
                vat_payer_code=entity_data.get('vat_code')
            )
            supplier = Supplier(
                entity=entity,
                bank_account=data['bank_account'],
                bank_name=data['bank_name'],
                id=data['id']
            )
            suppliers.append(supplier)
        return suppliers

    def sub_menu(self):
        while True:
            try:
                self._display_menu()
                choice = get_menu_input(MENU_PROMPT.format(min_value=1, max_value=len(SubMenuOption)), 1, len(SubMenuOption))
                selected_option = list(SubMenuOption)[int(choice)-1]
                if self.sub_menu_options[selected_option]() is False:
                    break
            except IndexError:
                print(INPUT_BETWEEN_VALUES.format(max_value=len(SubMenuOption)))
            except ValueError as ve:
                print("Value error:", ve) 
            except Exception as e:
                print(UNEXPECTED_ERROR.format(error=e))
                logging.error("Unexpected error in sub_menu", exc_info=True)


    def _display_menu(self):
        print(f"\n{SUPPLIER_MANAGER_HEADER}\n{DIVIDER}")
        for index, option in enumerate(SubMenuOption, start=1):
            print(f"{index}. {option.value}")


    def _handle_search_add_supplier(self):
        while True:
            print(f"\n{SEARCH_SUPPLIER_HEADER}\n{DIVIDER}")
            search_term = get_text_input("Enter supplier name or registration code to search: ")
            print("Searching...\n")
            results = self.company_searcher.search(search_term)
            if not results:
                print("No results found. Please try a different search term.")
                continue

            self.company_searcher.display_results(results)
            choice = get_menu_input(MENU_PROMPT_WITH_EXIT.format(min_value=1, max_value=len(results)), 1, len(results), allow_exit=True)
            if choice == "q":
                return

            selected_supplier = results[int(choice)-1]
            self._handle_selected_supplier(selected_supplier)
            break
        

    def _handle_selected_supplier(self, selected_supplier: JuridicalEntity):
        print(f"\n{SELECT_SUPPLIER_HEADER}\n{DIVIDER}")
        print(
            f"Name: {selected_supplier.name}\n"
            f"Registration code: {selected_supplier.registration_code}\n"
            f"Address: {selected_supplier.address}\n"
        )
        print(SUPPLIER_ADDITIONAL_INFO)
        supplier = get_user_input_VAT_bank_info(selected_supplier.name, selected_supplier.address, selected_supplier.registration_code)
        self._save_supplier(supplier)


    def _handle_add_supplier(self):
        print(f"\n{CREATE_SUPPLIER_HEADER}\n{DIVIDER}")
        supplier = get_user_input_supplier()
        self._save_supplier(supplier)

    def _save_supplier(self, supplier: Supplier):
        if get_confirmation("\nSave this profile? (y/n): "):
            self.json_handler.add_entry(supplier.to_dict())
            self.json_handler.save_json(SupplierManager.FILE_PATH)
            self.suppliers = self._load_suppliers_from_json()
            print(SUPPLIER_CREATED_MESSAGE)
        else:
            print(SUPPLIER_NOT_SAVED_MESSAGE)

    def _handle_view_suppliers(self):
        print(f"\n{SUPPLIER_LIST_HEADER}\n{DIVIDER}")
        self.display_suppliers()
        input(f"{Fore.YELLOW}Press Enter to continue...{Fore.RESET}")


    def _handle_delete_supplier(self):
        print(f"\n{DELETE_SUPPLIER_HEADER}\n{DIVIDER}")
        if not self.suppliers:
            print("No suppliers found.")
            return
        
        self.display_suppliers()
        choice = get_menu_input(MENU_PROMPT_WITH_EXIT.format(min_value=1, max_value=len(self.suppliers)), 1, len(self.suppliers), allow_exit=True)
        if choice == "q":
            return
        
        selected_supplier = self.suppliers[int(choice)-1]
        if get_confirmation(f"\nDelete {selected_supplier.entity.name} profile? (y/n): "):
            self.json_handler.delete_entry("id", str(selected_supplier.id))
            self.json_handler.save_json(SupplierManager.FILE_PATH)
            self.suppliers = self._load_suppliers_from_json()            
            print(f"{SUPPLIER_DELETED_MESSAGE}\n")
        else:
            print(SUPPLIER_NOT_DELETED_MESSAGE)

    def display_suppliers(self):
        for index, supplier in enumerate(self.suppliers, start=1):
            output = (
                f"{index}. \n"
                f"Name: {supplier.entity.name}\n"
                f"Registration code: {supplier.entity.registration_code}\n"
                f"Address: {supplier.entity.address}\n"
            )

            if supplier.entity.vat_payer_code:
                output += f"VAT code: {supplier.entity.vat_payer_code}\n"

            output += (
                f"Bank account: {supplier.bank_account}\n"
                f"Bank name: {supplier.bank_name}\n"
            )
            print(output)

        
    def _handle_return(self):
        return False
    