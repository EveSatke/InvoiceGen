from models.item import Item
from models.juridical_entity import JuridicalEntity
from models.physical_person import PhysicalPerson
from models.supplier import Supplier
from num2words import num2words


class Invoice:
    def __init__(self, invoice_number: str, invoice_date: str, supplier: Supplier, items: list[Item], buyer: JuridicalEntity | PhysicalPerson):
        self.invoice_number = invoice_number
        self.invoice_date = invoice_date
        self.supplier = supplier
        self.items = items
        self.buyer = buyer
        self.total_vat = self.calculate_total_vat()
        self.total_amount = self.calculate_total_amount()
        self.sum_in_words = num2words(self.total_amount, to='currency', lang="lt", currency="EUR")


    def calculate_total_vat(self):
        if self.supplier.entity.vat_payer_code:
            return sum(item.calculate_vat_amount() for item in self.items)
        return 0

    def calculate_total_amount(self):
        total_without_vat = sum(item.price * item.quantity for item in self.items)
        return total_without_vat + self.total_vat

    @property
    def invoice_number(self):
        return self._invoice_number
    
    @invoice_number.setter
    def invoice_number(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Invoice number must be a string")
        self._invoice_number = value

    @property
    def invoice_date(self):
        return self._invoice_date
    
    @invoice_date.setter
    def invoice_date(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Invoice date must be a string")
        self._invoice_date = value