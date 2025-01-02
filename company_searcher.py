from models.juridical_entity import JuridicalEntity


class CompanySearcher:
    def __init__(self, data: list):
        self.data = data

    def search(self, search_term: str):
        results = []
        for row in self.data:
            try:
                registration_code = int(row["ja_kodas"])
            except ValueError:
                print(f"Warning: Registration code '{row['ja_kodas']}' is not a valid integer.")
                
            
            if search_term.lower() in row["ja_pavadinimas"].lower() or search_term in str(registration_code):
                company = JuridicalEntity(
                    name = row["ja_pavadinimas"],
                    registration_code = registration_code,
                    address = row["adresas"],
                )
                results.append(company)
        return results