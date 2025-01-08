import asyncio
import os
import time

from colorama import Fore
from company_list_downloader import CompanyListDownloader
from company_searcher import CompanySearcher
from csv_reader import CsvReader
from invoice_data_manager import InvoiceDataManager
from invoice_manager import InvoiceManager
from menu_manager import MenuManager
from supplier_manager import SupplierManager
from json_handler import JsonHandler
from invoice_generator import InvoiceGenerator

URL = "https://www.registrucentras.lt/aduomenys/?byla=JAR_IREGISTRUOTI.csv"
FILENAME = "data/JAR_IREGISTRUOTI.csv"
BASE_DIRECTORY = "data/invoices"
INVOICE_FILENAME = "data/invoices.json"

CACHE_FILE = "data/last_download_time.txt"
"""Cache duration 24 hours in seconds"""
CACHE_DURATION = 86400  

async def download_companies_list():
    """Download the companies list if the cache is expired or doesn't exist"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            last_download_time = float(file.read().strip())
        
        if time.time() - last_download_time < CACHE_DURATION:
            print(f"{Fore.GREEN}Using cached company list file.{Fore.RESET}")
            return

    print(f"{Fore.YELLOW}Downloading companies list file... Please wait...{Fore.RESET}")
    downloader = CompanyListDownloader(URL, FILENAME)
    await downloader.download()

    with open(CACHE_FILE, 'w') as file:
        file.write(str(time.time()))

def setup_dependencies():
    """Download the company list before setting up dependencies"""
    asyncio.run(download_companies_list())

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
