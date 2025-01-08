from datetime import datetime
from enum import Enum
from typing import Optional
from colorama import Fore
from utils.company_searcher import CompanySearcher
from utils.constants import CREATE_PHYSICAL_PERSON_HEADER, DIVIDER, GENERATE_INVOICE_HEADER, INVOICE_SUMMARY_HEADER, MENU_PROMPT, MENU_PROMPT_WITH_EXIT, NO_RESULTS_FOUND, PRESS_ENTER, SEARCH_JURIDICAL_ENTITY_HEADER, VIEW_INVOICES_HEADER
from utils.input_handler import get_items_from_user, get_juridical_buyer_from_user, get_physical_buyer_from_user
from invoice_data_manager import InvoiceDataManager
from invoice_generator import InvoiceGenerator
from models.juridical_entity import JuridicalEntity
from models.physical_person import PhysicalPerson
from models.supplier import Supplier
from supplier_manager import SupplierManager
from utils.helpers import get_confirmation, get_menu_input, get_text_input, print_invoice_summary
from models.invoice import Invoice
from tabulate import tabulate

class Buyer(Enum):
    COMPANY = "Juridical entity"
    INDIVIDUAL = "Physical person"

class InvoiceManager:
    def __init__(self, supplier_manager: SupplierManager, company_searcher: CompanySearcher, invoice_generator: InvoiceGenerator, invoice_data_manager: InvoiceDataManager):
        self.supplier_manager = supplier_manager
        self.company_searcher = company_searcher
        self.invoice_generator = invoice_generator
        self.invoice_data_manager = invoice_data_manager

    def generate_invoice(self):
        supplier = self._select_supplier()
        if not supplier:
            return

        buyer = self._select_buyer_type()
        if not buyer:
            return
            
        items = self._add_invoice_items(supplier)
        invoice_date = datetime.now().strftime("%Y-%m-%d")
        
        invoice = Invoice(
            invoice_number=self._generate_invoice_number(supplier),
            invoice_date=invoice_date, 
            supplier=supplier,
            items=items,
            buyer=buyer,
        )

        self._get_invoice_summary(invoice)

        if get_confirmation("Generate this invoice? (y/n): "):
            self.invoice_generator.generate_invoice_pdf(invoice)
            self.invoice_data_manager.save_invoice(invoice)

    
    def _generate_invoice_number(self, supplier: Supplier) -> str:
        invoices = self.invoice_data_manager.load_invoices()
        current_year = datetime.now().year

        supplier_invoices = [
            invoice for invoice in invoices
            if invoice.supplier.entity.registration_code == supplier.entity.registration_code
            and invoice.invoice_date.startswith(str(current_year))
        ]

        max_sequence = 0
        for invoice in supplier_invoices:
            _, sequence = invoice.invoice_number.split('-')
            max_sequence = max(max_sequence, int(sequence))

        new_sequence = max_sequence + 1
        new_invoice_number = f"{current_year}-{new_sequence}"

        return new_invoice_number

    def _select_supplier(self) -> Optional[Supplier]:
        print(f"\n{GENERATE_INVOICE_HEADER}\n{DIVIDER}")
        print(f"{Fore.YELLOW}Step 1:{Fore.RESET} Select Supplier")
        if not self.supplier_manager.suppliers:
            print(f"{Fore.YELLOW}No suppliers found. Please create a supplier first.{Fore.RESET}")
            return 
        
        self.supplier_manager.display_suppliers()
        choice = get_menu_input(MENU_PROMPT_WITH_EXIT.format(min_value=1, max_value=len(self.supplier_manager.suppliers)), 1, len(self.supplier_manager.suppliers), allow_exit=True)
        if choice == "q":
            return 
        selected_supplier = self.supplier_manager.suppliers[int(choice)-1]
        return selected_supplier

    def _select_buyer_type(self) -> JuridicalEntity | PhysicalPerson | None:
        print(f"\n{GENERATE_INVOICE_HEADER}\n{DIVIDER}")
        print(f"{Fore.YELLOW}Step 2:{Fore.RESET} Select Buyer Type")
        for index, buyer in enumerate(Buyer, start=1):
            print(f"{index}. {buyer.value}")
        choice = get_menu_input(MENU_PROMPT.format(min_value=1, max_value=len(Buyer)), 1, len(Buyer))
        if choice == 1:
            return self._handle_search_juridical_buyer()
        elif choice == 2:
            return self._handle_physical_person_buyer()
        else:
            print("Invalid choice. Please try again.")
        
    def _handle_search_juridical_buyer(self) -> Optional[JuridicalEntity]:
        while True:
            print(f"\n{SEARCH_JURIDICAL_ENTITY_HEADER}\n{DIVIDER}")
            search_term = get_text_input("Enter company name or registration code to search: ")
            print("Searching...\n")
            results = self.company_searcher.search(search_term)
            if not results:
                print(NO_RESULTS_FOUND)
                continue

            self.company_searcher.display_results(results)
            choice = get_menu_input(MENU_PROMPT_WITH_EXIT.format(min_value=1, max_value=len(results)), 1, len(results), allow_exit=True)
            if choice == "q":
                return

            selected_entity = results[int(choice)-1]
            juridical_entity = get_juridical_buyer_from_user(selected_entity.name, selected_entity.address, selected_entity.registration_code)
            return juridical_entity

    def _handle_physical_person_buyer(self) -> PhysicalPerson:
        print(f"\n{CREATE_PHYSICAL_PERSON_HEADER}\n{DIVIDER}")
        physical_person = get_physical_buyer_from_user()
        return physical_person
    
    def _add_invoice_items(self, supplier: Supplier):
        print(f"\n{GENERATE_INVOICE_HEADER}\n{DIVIDER}")
        print(f"{Fore.YELLOW}Step 3:{Fore.RESET} Add Items")
        items = get_items_from_user(supplier)
        return items
    
    def _get_invoice_summary(self, invoice: Invoice):
        print(f"\n{INVOICE_SUMMARY_HEADER}\n{DIVIDER}")
        print_invoice_summary(invoice)

    def view_invoices(self):
        invoices = self.invoice_data_manager.load_invoices()
        print(f"\n{VIEW_INVOICES_HEADER}\n{DIVIDER}")
        if not invoices:
            print(f"{Fore.YELLOW}No invoices found.{Fore.RESET}")
            return
        
        table_data = []
        for invoice in invoices:
            table_data.append([
                f"{invoice.invoice_number}",
                f"{invoice.invoice_date}",
                f"{invoice.supplier.entity.name}",
                f"{invoice.buyer.name}",
                f"{invoice.total_amount:.2f} EUR"
            ])

        headers = [
        f"{Fore.YELLOW}Invoice No.{Fore.RESET}",
        f"{Fore.YELLOW}Date{Fore.RESET}",
        f"{Fore.YELLOW}Supplier{Fore.RESET}",
        f"{Fore.YELLOW}Buyer{Fore.RESET}",
        f"{Fore.YELLOW}Total Amount{Fore.RESET}"
        ]
            
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        input(PRESS_ENTER)
