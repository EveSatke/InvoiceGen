from datetime import datetime
from enum import Enum
from typing import Optional
from colorama import Fore
from company_searcher import CompanySearcher
from constants import CREATE_PHYSICAL_PERSON_HEADER, DIVIDER, GENERATE_INVOICE_HEADER, INVOICE_SUMMARY_HEADER, MENU_PROMPT, MENU_PROMPT_WITH_EXIT, SEARCH_JURIDICAL_ENTITY_HEADER
from input_handler import get_item_input, get_user_input_juridical_buyer, get_user_input_physical_person_buyer
from json_handler import JsonHandler
from models.item import Item
from models.juridical_entity import JuridicalEntity
from models.physical_person import PhysicalPerson
from models.supplier import Supplier
import supplier_manager
from utils.helpers import get_confirmation, get_menu_input, get_text_input, get_vat_code
from models.invoice import Invoice

class Buyer(Enum):
    COMPANY = "Juridical entity"
    INDIVIDUAL = "Physical person"

class InvoiceGenerator:
    def __init__(self, supplier_manager: supplier_manager.SupplierManager, company_searcher: CompanySearcher):
        self.supplier_manager = supplier_manager
        self.company_searcher = company_searcher

    def generate_invoice(self):
        supplier = self._select_supplier()
        if not supplier:
            return

        buyer = self._select_buyer_type()
        items = self._add_invoice_items(supplier)
        invoice_date = datetime.now().strftime("%Y-%m-%d")
        
        invoice = Invoice(
            invoice_number="INV-001",  # Example invoice number
            invoice_date=invoice_date,  # Example invoice date
            supplier=supplier,
            buyer=buyer,
            items=items,
            )

        total_vat = invoice.calculate_total_vat()
        total_amount = invoice.calculate_total_amount()
        print(invoice.sum_in_words)

        self._get_invoice_summary(supplier, buyer, items, total_vat, total_amount)

        if get_confirmation("Generate this invoice? (y/n): "):
            # Logic to save or generate the invoice PDF
            pass
    
    def _generate_invoice_number(self) -> str:
        ...

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
        print(selected_supplier)
        return selected_supplier

    def _select_buyer_type(self):
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
                print("No results found. Please try a different search term.")
                continue

            self.company_searcher.display_results(results)
            choice = get_menu_input(MENU_PROMPT_WITH_EXIT.format(min_value=1, max_value=len(results)), 1, len(results), allow_exit=True)
            if choice == "q":
                return

            selected_entity = results[int(choice)-1]
            juridical_entity = get_user_input_juridical_buyer(selected_entity.name, selected_entity.address, selected_entity.registration_code)
            return juridical_entity

    def _handle_physical_person_buyer(self) -> PhysicalPerson:
        print(f"\n{CREATE_PHYSICAL_PERSON_HEADER}\n{DIVIDER}")
        physical_person = get_user_input_physical_person_buyer()
        return physical_person
    
    def _add_invoice_items(self, supplier: Supplier):
        print(f"\n{GENERATE_INVOICE_HEADER}\n{DIVIDER}")
        print(f"{Fore.YELLOW}Step 3:{Fore.RESET} Add Items")
        items = get_item_input(supplier)
        return items
    
    def _get_invoice_summary(self, supplier: Supplier, buyer: JuridicalEntity | PhysicalPerson, items: list[Item], total_vat: float, total_amount: float):
        def print_supplier_details(supplier: Supplier):
            print(
                f"{Fore.YELLOW}Supplier:\n{Fore.RESET}"
                f"Name: {supplier.entity.name}\n"
                f"Address: {supplier.entity.address}\n"
                f"Registration code: {supplier.entity.registration_code}\n"
                f"VAT code: {supplier.entity.vat_payer_code}\n"
                f"Bank account: {supplier.bank_account}\n"
                f"Bank name: {supplier.bank_name}\n"
            )

        def print_buyer_details(buyer: JuridicalEntity | PhysicalPerson):
            print(f"{Fore.YELLOW}Buyer: {Fore.RESET}")
            if isinstance(buyer, JuridicalEntity):
                print(
                    f"Name: {buyer.name}\n"
                    f"Address: {buyer.address}\n"
                    f"Registration code: {buyer.registration_code}\n"
                    f"VAT payer code: {buyer.vat_payer_code}\n"
                )
            elif isinstance(buyer, PhysicalPerson):
                print(
                    f"Name: {buyer.name}\n"
                    f"Surname: {buyer.surname}\n"
                    f"Address: {buyer.address}\n"
                    f"VAT payer code: {buyer.vat_payer_code}\n"
                )

        def print_items_details(items: list[Item]):
            print(f"{Fore.YELLOW}Items: {Fore.RESET}")
            for index, item in enumerate(items, start=1):
                print(f"{index}. {item.name} - {item.quantity} X {item.price} EUR = {item.price * item.quantity} EUR")

        print(f"\n{INVOICE_SUMMARY_HEADER}\n{DIVIDER}")
        print_supplier_details(supplier)
        print_buyer_details(buyer)
        print_items_details(items)

        if supplier.entity.vat_payer_code:
            print(f"\nTotal VAT: {total_vat} EUR")
        print(f"{Fore.YELLOW}\nTotal Amount: {total_amount} EUR{Fore.RESET}")
