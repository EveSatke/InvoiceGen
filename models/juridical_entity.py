from models.entity import Entity

class JuridicalEntity(Entity):
    def __init__(self, name: str, address: str, registration_code: int, vat_payer_code: str | None = None):
        super().__init__(vat_payer_code)
        self.name = name
        self.address = address
        self.registration_code = registration_code

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Company name must be a string")
        self._name = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Address must be a string")
        self._address = value

    @property
    def registration_code(self):
        return self._registration_code
    
    @registration_code.setter
    def registration_code(self, value: int):
        if not isinstance(value, int) and len(str(value)) != 9:
            raise ValueError("Registration code must be 9 digits long")
        self._registration_code = value

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "registration_code": self.registration_code,
            "vat_payer_code": self.vat_payer_code
        }

    def get_entity_info(self):
        return (f"Company Name: {self.name}, Code: {self.registration_code}, "
                f"Address: {self.address}, {self.get_vat_info()}")