from company_searcher import CompanySearcher
from csv_reader import CsvReader
from invoice_data_manager import InvoiceDataManager
from invoice_manager import InvoiceManager
from menu_manager import MenuManager
from supplier_manager import SupplierManager
from json_handler import JsonHandler
from invoice_generator import InvoiceGenerator
FILENAME = "data/JAR_IREGISTRUOTI.csv"
BASE_DIRECTORY = "data/invoices"
INVOICE_FILENAME = "data/invoices.json"
def setup_dependencies():
    json_handler = JsonHandler()
    csv_reader = CsvReader(FILENAME)
    data = csv_reader.read()
    company_searcher = CompanySearcher(data)
    invoice_generator = InvoiceGenerator(BASE_DIRECTORY)
    invoice_data_manager = InvoiceDataManager(json_handler, INVOICE_FILENAME)
    supplier_manager = SupplierManager(json_handler, company_searcher)
    invoice_manager = InvoiceManager(supplier_manager, company_searcher, invoice_generator, invoice_data_manager)
    menu = MenuManager(supplier_manager, invoice_manager)
    return menu
