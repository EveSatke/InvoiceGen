from models.juridical_entity import JuridicalEntity
from models.physical_person import PhysicalPerson

class Supplier:
    def __init__(self, entity, bank_account, bank_name):
        self.entity = entity
        self.bank_account = bank_account
        self.bank_name = bank_name

    @property
    def entity(self):
        return self._entity
    
    @entity.setter
    def entity(self, value: JuridicalEntity | PhysicalPerson):
        if not isinstance(value, (JuridicalEntity, PhysicalPerson)):
            raise ValueError("Entity must be a JuridicalEntity or PhysicalPerson")
        self._entity = value

    @property
    def bank_account(self):
        return self._bank_account
    
    @bank_account.setter
    def bank_account(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Bank account must be a string")
        self._bank_account = value

    @property
    def bank_name(self):
        return self._bank_name
    
    @bank_name.setter
    def bank_name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Bank name must be a string")
        self._bank_name = value
    
    def get_supplier_info(self):
        entity_info = self.entity.get_entity_info()
        return (f"{entity_info}, Bank Account: {self.bank_account}, Bank Name: {self.bank_name}")