class Item:
    def __init__(self, name:str, quantity: int, price: float, vat_rate: float=0):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.vat_rate = vat_rate


    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Quantity must be an integer")
        self._quantity = value

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value: float):
        if not isinstance(value, float):
            raise ValueError("Price must be a float")
        self._price = value

    @property
    def vat_rate(self):
        return self._vat_rate
    
    @vat_rate.setter
    def vat_rate(self, value: float):
        if not isinstance(value, float):
            raise ValueError("VAT rate must be a float")
        self._vat_rate = value
    
    def calculate_vat_amount(self):
        return self.price * self.quantity * (self.vat_rate / 100)

    def __str__(self):
        return f"Item: {self.name}, Quantity: {self.quantity}, Price: {self.price}, VAT Rate: {self.vat_rate}%"
    
    def __repr__(self):
        return f"Item: {self.name}, Quantity: {self.quantity}, Price: {self.price}, VAT Rate: {self.vat_rate}%"
