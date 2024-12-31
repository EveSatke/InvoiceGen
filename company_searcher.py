from models.juridical_entity import JuridicalEntity


class CompanySearcher:
    def __init__(self, data: list):
        self.data = data

    def search(self, search_term: str):
        results = []
        for row in self.data:
            if search_term in row["ja_pavadinimas"].lower() or search_term in row["ja_kodas"]:
                company = JuridicalEntity(
                    name = row["ja_pavadinimas"],
                    registration_code = row["ja_kodas"],
                    address = row["adresas"],
                )
                results.append(company)
        return results