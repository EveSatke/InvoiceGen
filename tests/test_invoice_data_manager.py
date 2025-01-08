import pytest
from unittest.mock import MagicMock
from src.invoice_data_manager import InvoiceDataManager
from src.models.invoice import Invoice
from src.models.item import Item
from src.models.juridical_entity import JuridicalEntity
from src.models.physical_person import PhysicalPerson
from src.models.supplier import Supplier
import uuid

@pytest.fixture
def json_handler():
    return MagicMock()

@pytest.fixture
def invoice_data_manager(json_handler):
    return InvoiceDataManager(json_handler, "test_invoices.json")

def test_save_invoice(invoice_data_manager, json_handler):
    supplier = Supplier(
        entity=JuridicalEntity("Test Supplier", "Test Address", 123456789),
        bank_account="LT123456789",
        bank_name="Test Bank",
        id=str(uuid.uuid4())
    )
    buyer = JuridicalEntity("Test Buyer", "Buyer Address", 987654321)
    items = [Item("Test Item", 1, 100.0, 21.0)]
    invoice = Invoice(
        invoice_number="2025-1",
        invoice_date="2025-01-01",
        supplier=supplier,
        items=items,
        buyer=buyer
    )

    invoice_data_manager.save_invoice(invoice)

    json_handler.save.assert_called_once_with("test_invoices.json", invoice.to_dict())

def test_load_invoices(invoice_data_manager, json_handler):
    supplier_data = {
        "id": str(uuid.uuid4()),
        "entity": {
            "name": "Test Supplier",
            "address": "Test Address",
            "registration_code": 123456789,
            "vat_payer_code": None
        },
        "bank_account": "LT123456789",
        "bank_name": "Test Bank"
    }
    buyer_data = {
        "name": "Test Buyer",
        "address": "Buyer Address",
        "registration_code": 987654321,
        "vat_payer_code": None
    }
    item_data = {
        "name": "Test Item",
        "quantity": 1,
        "price": 100.0,
        "vat_rate": 21.0
    }
    invoice_data = [{
        "invoice_number": "2025-1",
        "invoice_date": "2025-01-01",
        "supplier": supplier_data,
        "items": [item_data],
        "buyer": buyer_data
    }]
    json_handler.load_json.return_value = invoice_data

    invoices = invoice_data_manager.load_invoices()

    assert len(invoices) == 1
    assert invoices[0].invoice_number == "2025-1"
    assert invoices[0].supplier.entity.name == "Test Supplier"
    assert invoices[0].buyer.name == "Test Buyer"
    assert len(invoices[0].items) == 1
    assert invoices[0].items[0].name == "Test Item"
