from models.item import Item
from models.juridical_entity import JuridicalEntity
from models.physical_person import PhysicalPerson
from models.supplier import Supplier


class Invoice:
    def __init__(self, invoice_number: str, invoice_date: str, supplier: Supplier, entity: JuridicalEntity | PhysicalPerson,items: list[Item]):
        self.invoice_number = invoice_number
        self.invoice_date = invoice_date
        self.supplier = supplier
        self.items = items
        self.entity = entity

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

    @property
    def supplier(self):
        return self._supplier

    @supplier.setter
    def supplier(self, value: Supplier):
        if not isinstance(value, Supplier):
            raise ValueError("Supplier must be a Supplier")
        self._supplier = value

    @property
    def items(self):
        return self._items
    
    @items.setter
    def items(self, value: list[Item]):
        if not isinstance(value, list):
            raise ValueError("Items must be a list")
        self._items = value

    def get_invoice_info(self):
        supplier_info = self.supplier.get_supplier_info()
        entity_info = self.entity.get_entity_info()
        items_info = ", ".join(str(item) for item in self.items)
        return f"Supplier: {supplier_info}, Entity: {entity_info}, Items: {items_info}"