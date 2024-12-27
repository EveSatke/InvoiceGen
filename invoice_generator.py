from csv_reader import CompanySearcher, CsvReader
from company_list_downloader import CompanyListDownloader
from utils.helpers import get_text_input

URL = "https://www.registrucentras.lt/aduomenys/?byla=JAR_IREGISTRUOTI.csv"
FILENAME = "data/JAR_IREGISTRUOTI.csv"


async def start():
    # print("Downloading companies list file... Please wait...")
    # downloader = CompanyListDownloader(URL, FILENAME)
    # await downloader.download()
    search_term = get_text_input("Enter the name of the company: ")
    company_storage = CsvReader(FILENAME)
    company_searcher = CompanySearcher(search_term, company_storage.read())
    results = company_searcher.search()
    for entity in results:
        print(entity.company_code, entity.company_name, entity.address)

