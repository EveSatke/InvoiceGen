from enum import Enum
from constants import INPUT_BETWEEN_VALUES, INVOICE_GENERATOR_TITLE, MENU_PROMPT
from invoice_generator import InvoiceGenerator
from supplier_manager import SupplierManager
from utils.helpers import get_menu_input
from colorama import Fore


URL = "https://www.registrucentras.lt/aduomenys/?byla=JAR_IREGISTRUOTI.csv"



async def start():
    # print("Downloading companies list file... Please wait...")
    # downloader = CompanyListDownloader(URL, FILENAME)
    # await downloader.download()
    # print(get_user_input())
    ...

class MenuOption(Enum):
    ADD_INVOICE = "Add a new invoice"
    VIEW_INVOICES = "View all invoices"
    MANAGE_SUPPLIERS = "Manage supplier profiles"
    EXIT = "Exit"

class MenuManager:
    def __init__(self, supplier_manager: SupplierManager, invoice_generator: InvoiceGenerator):
        self.supplier_manager = supplier_manager
        self.invoice_generator = invoice_generator
        self.menu_options = {
            MenuOption.ADD_INVOICE: self._handle_add_invoice,
            MenuOption.VIEW_INVOICES: self._handle_view_invoices,
            MenuOption.MANAGE_SUPPLIERS: self._handle_manage_suppliers,
            MenuOption.EXIT: self._handle_exit
        }

    def main_menu(self):
        while True:
            self._display_menu()
            choice = get_menu_input(MENU_PROMPT.format(min_value=1, max_value=len(MenuOption)), 1, len(MenuOption))
            try:
                selected_option = list(MenuOption)[int(choice)-1]
                if self.menu_options[selected_option]() is False:
                    break
            except (IndexError, ValueError) as e:
                print(INPUT_BETWEEN_VALUES.format(min_value=1, max_value=len(MenuOption)))
                print(e)


    def _display_menu(self):
        print(INVOICE_GENERATOR_TITLE)
        for index, option in enumerate(MenuOption, start=1):
            print(f"{index}. {option.value}")


    def _handle_add_invoice(self):
        self.invoice_generator.generate_invoice()
        return True

    def _handle_view_invoices(self):
        return True

    def _handle_manage_suppliers(self):
        self.supplier_manager.sub_menu()


    def _handle_exit(self):
        print(f"{Fore.YELLOW}Exiting...\n{Fore.RESET}")
        return False
    

    

    