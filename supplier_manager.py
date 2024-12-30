from enum import Enum

from colorama import Fore
import logging
from constants import CREATE_SUPPLIER_HEADER, MENU_PROMPT, INVALID_OPTION_MESSAGE, INPUT_MUST_BE_NUMBER, SUPPLIER_CREATED_MESSAGE, SUPPLIER_NOT_SAVED_MESSAGE, UNEXPECTED_ERROR, SUPPLIER_MANAGER_HEADER, DIVIDER

from input_handler import get_user_input_supplier
from models.supplier import Supplier
from utils.helpers import get_confirmation, get_menu_input


class SubMenuOption(Enum):
    ADD_SUPPLIER = "Create a new supplier"
    VIEW_SUPPLIERS = "View all suppliers"
    DELETE_SUPPLIER = "Delete a supplier"
    EXIT = "Return to main menu"

class SupplierManager:
    def __init__(self):
        self.sub_menu_options = {
            SubMenuOption.ADD_SUPPLIER: self._handle_add_supplier,
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

    def _handle_add_supplier(self):
        print(f"\n{CREATE_SUPPLIER_HEADER}\n{DIVIDER}")
        supplier = get_user_input_supplier()
        if get_confirmation("Save this profile? (y/n): "):
            self._save_supplier(supplier)
            print(SUPPLIER_CREATED_MESSAGE)
        else:
            print(SUPPLIER_NOT_SAVED_MESSAGE)

    def _handle_view_suppliers(self):
        ...

    def _handle_delete_supplier(self):
        ...

    def _handle_return(self):
        return False
    
    def _save_supplier(self, supplier: Supplier):
        ...