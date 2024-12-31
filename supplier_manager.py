from enum import Enum
from colorama import Fore
import logging
from company_searcher import CompanySearcher
from constants import CREATE_SUPPLIER_HEADER, MENU_PROMPT, INVALID_OPTION_MESSAGE, INPUT_MUST_BE_NUMBER, SEARCH_RESULTS_HEADER, SEARCH_SUPPLIER_HEADER, SELECT_SUPPLIER_HEADER, SUPPLIER_ADDITIONAL_INFO, SUPPLIER_CREATED_MESSAGE, SUPPLIER_NOT_SAVED_MESSAGE, UNEXPECTED_ERROR, SUPPLIER_MANAGER_HEADER, DIVIDER
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
        self.suppliers = self.json_handler.load_json(SupplierManager.FILE_PATH)
        self.sub_menu_options = {
            SubMenuOption.SEARCH_ADD_SUPPLIER: self._handle_search_add_supplier,
            SubMenuOption.ADD_MANUALLY_SUPPLIER: self._handle_add_supplier,
            SubMenuOption.VIEW_SUPPLIERS: self._handle_view_suppliers,
            SubMenuOption.DELETE_SUPPLIER: self._handle_delete_supplier,
            SubMenuOption.EXIT: self._handle_return
        }

    def sub_menu(self):
        while True:
            try:
                self._display_menu()
                choice = get_menu_input(MENU_PROMPT.format(max_option=len(SubMenuOption)), 1, len(SubMenuOption))
                selected_option = list(SubMenuOption)[choice-1]
                if self.sub_menu_options[selected_option]() is False:
                    break
            except IndexError:
                print(INVALID_OPTION_MESSAGE.format(max_option=len(SubMenuOption)))
            except ValueError:
                print(INPUT_MUST_BE_NUMBER)
            except Exception as e:
                print(UNEXPECTED_ERROR.format(error=e))
                logging.error("Unexpected error in sub_menu", exc_info=True)

    def _display_menu(self):
        print(f"\n{SUPPLIER_MANAGER_HEADER}\n{DIVIDER}")
        for index, option in enumerate(SubMenuOption, start=1):
            print(f"{index}. {option.value}")


    def _handle_search_add_supplier(self):
        print(f"\n{SEARCH_SUPPLIER_HEADER}\n{DIVIDER}")
        search_term = get_text_input("Enter supplier name or registration code to search: ")
        print("Searching...\n")
        results = self.company_searcher.search(search_term)
        self._display_results(results)
        choice = get_menu_input(MENU_PROMPT.format(max_option=len(results)), 1, len(results))
        selected_supplier = results[choice-1]
        self._handle_selected_supplier(selected_supplier)
        

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


    def _display_results(self, results: list):
        print(f"SEARCH_RESULTS_HEADER\n{DIVIDER}")
        if not results:
            print("No results found")
            return
        for index, company in enumerate(results, start=1):
            print(f"{index}. Name: {company.name} | Registration code: {company.registration_code} | Address: {company.address}")

    def _handle_add_supplier(self):
        print(f"\n{CREATE_SUPPLIER_HEADER}\n{DIVIDER}")
        supplier = get_user_input_supplier()
        self._save_supplier(supplier)

    def _save_supplier(self, supplier: Supplier):
        if get_confirmation("\nSave this profile? (y/n): "):
            self.json_handler.add_entry(supplier.to_dict())
            self.json_handler.save_json(SupplierManager.FILE_PATH)
            print(SUPPLIER_CREATED_MESSAGE)
        else:
            print(SUPPLIER_NOT_SAVED_MESSAGE)

    def _handle_view_suppliers(self):
        ...

    def _handle_delete_supplier(self):
        ...

    def _handle_return(self):
        return False
    