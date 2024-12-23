import csv
from models.juridical_entity import JuridicalEntity


class CsvReader:
    def __init__(self, filename, delimiter='|'):
        self.filename = filename
        self.delimiter = delimiter

    def read(self):
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file, delimiter=self.delimiter)
            return list(reader)
        
class CompanySearcher:
    def __init__(self, search_term: str, data: list):
        self.search_term = search_term
        self.data = data

    def search(self):
        results = []
        for row in self.data:
            if self.search_term in row["ja_pavadinimas"].lower():
                company = JuridicalEntity(
                    company_code = row["ja_kodas"],
                    company_name = row["ja_pavadinimas"],
                    address = row["adresas"],
                )
                results.append(company)
        return results