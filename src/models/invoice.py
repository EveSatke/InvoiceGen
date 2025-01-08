from .item import Item
from .juridical_entity import JuridicalEntity
from .physical_person import PhysicalPerson
from .supplier import Supplier
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
            total_vat = sum(item.calculate_vat_amount() for item in self.items)
            return round(total_vat, 2)
        return 0.00

    def calculate_total_amount(self):
        total_without_vat = sum(item.price * item.quantity for item in self.items)
        total_amount = total_without_vat + self.total_vat
        return round(total_amount, 2)

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

    def to_dict(self):
        return {
            "invoice_number": self.invoice_number,
            "invoice_date": self.invoice_date,
            "supplier": self.supplier.to_dict(),
            "buyer": self.buyer.to_dict(),
            "items": [item.to_dict() for item in self.items],
            "total_vat": self.total_vat,
            "total_amount": self.total_amount,
            "sum_in_words": self.sum_in_words
        }