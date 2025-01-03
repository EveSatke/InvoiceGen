from company_searcher import CompanySearcher
from csv_reader import CsvReader
from invoice_generator import InvoiceGenerator
from menu_manager import MenuManager
from supplier_manager import SupplierManager
from json_handler import JsonHandler

FILENAME = "data/JAR_IREGISTRUOTI.csv"

def setup_dependencies():
    json_handler = JsonHandler()
    csv_reader = CsvReader(FILENAME)
    data = csv_reader.read()
    company_searcher = CompanySearcher(data)
    supplier_manager = SupplierManager(json_handler, csv_reader, company_searcher)
    invoice_generator = InvoiceGenerator(supplier_manager, company_searcher)
    menu = MenuManager(supplier_manager, invoice_generator)
    return menu
