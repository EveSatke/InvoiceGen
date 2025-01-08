from .juridical_entity import JuridicalEntity
from .physical_person import PhysicalPerson
import uuid


class Supplier:
    def __init__(self, entity: JuridicalEntity, bank_account: str, bank_name: str, id: str):
        self.id = uuid.UUID(id) if id else uuid.uuid4()
        self.entity = entity
        self.bank_account = bank_account
        self.bank_name = bank_name

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

    def to_dict(self):
        return {
            "id": str(self.id),
            "entity": self.entity.to_dict(),
            "bank_account": self.bank_account,
            "bank_name": self.bank_name
        }
    
    def get_supplier_info(self):
        entity_info = self.entity.get_entity_info()
        return (f"{entity_info}, Bank Account: {self.bank_account}, Bank Name: {self.bank_name}")