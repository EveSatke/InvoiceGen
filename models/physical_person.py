from models.entity import Entity

class PhysicalPerson(Entity):
    def __init__(self, name, surname, address, vat_payer_code=None):
        super().__init__(vat_payer_code)
        self.name = name
        self.surname = surname
        self.address = address

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value

    @property
    def surname(self):
        return self._surname
    
    @surname.setter
    def surname(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Surname must be a string")
        self._surname = value

    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Address must be a string")
        self._address = value

    def get_entity_info(self):
        return (f"Name: {self.name} {self.surname}, Address: {self.address}, "
                f"{self.get_vat_info()}") 