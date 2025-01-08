from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, vat_payer_code: str | None = None):
        self.vat_payer_code = vat_payer_code

    @property
    def vat_payer_code(self):
        return self._vat_payer_code
    
    @vat_payer_code.setter
    def vat_payer_code(self, value: str | None):
        if value is not None and not isinstance(value, str):
            raise ValueError("VAT Payer Code must be a string")
        self._vat_payer_code = value

    @abstractmethod
    def get_entity_info(self):
        pass

    def get_vat_info(self):
        return f"VAT Payer Code: {self.vat_payer_code}" if self.vat_payer_code else "Not a VAT Payer"
