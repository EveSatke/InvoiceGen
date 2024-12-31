import asyncio
from invoice_generator import InvoiceGenerator
from supplier_manager import SupplierManager
from json_handler import JsonHandler



def main():
    # asyncio.run(invoice_generator.start())
    json_handler = JsonHandler()
    supplier_manager = SupplierManager(json_handler)
    generator = InvoiceGenerator(supplier_manager)
    generator.main_menu()

if __name__ == "__main__":
    main()
