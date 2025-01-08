import pytest
from unittest.mock import patch, MagicMock
from src.invoice_manager import InvoiceManager
from src.supplier_manager import SupplierManager
from src.utils.company_searcher import CompanySearcher
from src.invoice_generator import InvoiceGenerator
from src.invoice_data_manager import InvoiceDataManager
from src.models.supplier import Supplier
from src.models.juridical_entity import JuridicalEntity
from src.models.item import Item
import uuid
from datetime import datetime

@pytest.fixture
def invoice_manager():
    supplier_manager = MagicMock(spec=SupplierManager)
    company_searcher = MagicMock(spec=CompanySearcher)
    invoice_generator = MagicMock(spec=InvoiceGenerator)
    invoice_data_manager = MagicMock(spec=InvoiceDataManager)

    return InvoiceManager(
        supplier_manager,
        company_searcher,
        invoice_generator,
        invoice_data_manager
    )

# Mock both get_confirmation and input
@patch('builtins.input', return_value='y')
@patch('src.utils.helpers.get_confirmation', return_value=True)
def test_generate_invoice(mock_get_confirmation, mock_input, invoice_manager):
    supplier = Supplier(
        entity=JuridicalEntity("Test Supplier", "Test Address", 123456789),
        bank_account="LT123456789",
        bank_name="Test Bank",
        id=str(uuid.uuid4())
    )
    buyer = JuridicalEntity("Test Buyer", "Buyer Address", 987654321)
    items = [Item("Test Item", 1, 100.0, 21.0)]

    invoice_manager._select_supplier = MagicMock(return_value=supplier)
    invoice_manager._select_buyer_type = MagicMock(return_value=buyer)
    invoice_manager._add_invoice_items = MagicMock(return_value=items)
    invoice_manager._generate_invoice_number = MagicMock(return_value="2025-1")
    invoice_manager._get_invoice_summary = MagicMock()

    invoice_manager.generate_invoice()

    invoice_manager.invoice_generator.generate_invoice_pdf.assert_called_once()
    invoice_manager.invoice_data_manager.save_invoice.assert_called_once()

def test_generate_invoice_no_supplier(invoice_manager):
    invoice_manager._select_supplier = MagicMock(return_value=None)

    invoice_manager.generate_invoice()

    invoice_manager.invoice_generator.generate_invoice_pdf.assert_not_called()
    invoice_manager.invoice_data_manager.save_invoice.assert_not_called()

def test_generate_invoice_no_buyer(invoice_manager):
    supplier = Supplier(
        entity=JuridicalEntity("Test Supplier", "Test Address", 123456789),
        bank_account="LT123456789",
        bank_name="Test Bank",
        id=str(uuid.uuid4())
    )
    invoice_manager._select_supplier = MagicMock(return_value=supplier)
    invoice_manager._select_buyer_type = MagicMock(return_value=None)

    invoice_manager.generate_invoice()

    invoice_manager.invoice_generator.generate_invoice_pdf.assert_not_called()
    invoice_manager.invoice_data_manager.save_invoice.assert_not_called()

# Mock both get_confirmation and input
@patch('builtins.input', return_value='n')
@patch('src.utils.helpers.get_confirmation', return_value=False)
def test_generate_invoice_no_items(mock_get_confirmation, mock_input, invoice_manager):
    supplier = Supplier(
        entity=JuridicalEntity("Test Supplier", "Test Address", 123456789),
        bank_account="LT123456789",
        bank_name="Test Bank",
        id=str(uuid.uuid4())
    )
    buyer = JuridicalEntity("Test Buyer", "Buyer Address", 987654321)
    invoice_manager._select_supplier = MagicMock(return_value=supplier)
    invoice_manager._select_buyer_type = MagicMock(return_value=buyer)
    invoice_manager._add_invoice_items = MagicMock(return_value=[])

    invoice_manager.generate_invoice()

    invoice_manager.invoice_generator.generate_invoice_pdf.assert_not_called()
    invoice_manager.invoice_data_manager.save_invoice.assert_not_called()

def test_generate_invoice_number(invoice_manager):
    supplier = Supplier(
        entity=JuridicalEntity("Test Supplier", "Test Address", 123456789),
        bank_account="LT123456789",
        bank_name="Test Bank",
        id=str(uuid.uuid4())
    )
    invoice_manager.invoice_data_manager.load_invoices = MagicMock(return_value=[])

    invoice_number = invoice_manager._generate_invoice_number(supplier)

    assert invoice_number == f"{datetime.now().year}-1"

# Mock both get_confirmation and input
@patch('builtins.input', return_value='y')
@patch('src.utils.helpers.get_confirmation', return_value=True)
def test_get_invoice_summary(mock_get_confirmation, mock_input, invoice_manager):
    supplier = Supplier(
        entity=JuridicalEntity("Test Supplier", "Test Address", 123456789),
        bank_account="LT123456789",
        bank_name="Test Bank",
        id=str(uuid.uuid4())
    )
    buyer = JuridicalEntity("Test Buyer", "Buyer Address", 987654321)
    items = [Item("Test Item", 1, 100.0, 21.0)]

    invoice_manager._select_supplier = MagicMock(return_value=supplier)
    invoice_manager._select_buyer_type = MagicMock(return_value=buyer)
    invoice_manager._add_invoice_items = MagicMock(return_value=items)
    invoice_manager._generate_invoice_number = MagicMock(return_value="2025-1")
    invoice_manager._get_invoice_summary = MagicMock()

    invoice_manager.generate_invoice()

    invoice_manager._get_invoice_summary.assert_called_once()
    called_invoice = invoice_manager._get_invoice_summary.call_args[0][0]

    assert called_invoice.supplier == supplier
    assert called_invoice.buyer == buyer
    assert called_invoice.items == items
    assert called_invoice.invoice_number == "2025-1"

def test_add_supplier(invoice_manager):
    supplier_data = {
        "name": "Test Supplier",
        "address": "Test Address",
        "registration_code": 123456789,
        "vat_payer_code": None,
        "bank_account": "LT123456789",
        "bank_name": "Test Bank"
    }
    supplier = Supplier(
        entity=JuridicalEntity(
            supplier_data["name"],
            supplier_data["address"],
            supplier_data["registration_code"],
            supplier_data["vat_payer_code"]
        ),
        bank_account=supplier_data["bank_account"],
        bank_name=supplier_data["bank_name"],
        id=str(uuid.uuid4())
    )

    invoice_manager.supplier_manager.add_supplier = MagicMock()

    invoice_manager.supplier_manager.add_supplier(supplier)

    invoice_manager.supplier_manager.add_supplier.assert_called_once_with(supplier)
