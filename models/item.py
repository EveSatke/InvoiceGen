class Item:
    def __init__(self, name:str, quantity: int, price: float):
        self.name = name
        self.quantity = quantity
        self.price = price


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
    
    def __str__(self):
        return f"Item: {self.name}, Quantity: {self.quantity}, Price: {self.price}"
    
    def __repr__(self):
        return f"Item: {self.name}, Quantity: {self.quantity}, Price: {self.price}"
