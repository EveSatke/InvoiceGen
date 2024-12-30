import asyncio
from invoice_generator import InvoiceGenerator
from supplier_manager import SupplierManager



def main():
    # asyncio.run(invoice_generator.start())
    supplier_manager = SupplierManager()
    generator = InvoiceGenerator(supplier_manager)
    generator.main_menu()

if __name__ == "__main__":
    main()
