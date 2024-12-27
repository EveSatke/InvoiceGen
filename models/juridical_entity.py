from models.entity import Entity

class JuridicalEntity(Entity):
    def __init__(self, company_name: str, company_code: int, address: str, vat_payer_code: str | None = None):
        super().__init__(vat_payer_code)
        self.company_name = company_name
        self.company_code = company_code
        self.address = address

    @property
    def company_name(self):
        return self._company_name
    
    @company_name.setter
    def company_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Company name must be a string")
        self._company_name = value

    @property
    def company_code(self):
        return self._company_code
    
    @company_code.setter
    def company_code(self, value: int):
        if not isinstance(value, int) and len(str(value)) != 9:
            raise ValueError("Company code must be 9 digits long")
        self._company_code = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Address must be a string")
        self._address = value

    def get_entity_info(self):
        return (f"Company Name: {self.company_name}, Code: {self.company_code}, "
                f"Address: {self.address}, {self.get_vat_info()}")