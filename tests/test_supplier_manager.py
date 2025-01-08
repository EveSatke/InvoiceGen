import pytest
from unittest.mock import patch, MagicMock
from src.supplier_manager import SupplierManager
from src.utils.json_handler import JsonHandler
from src.utils.company_searcher import CompanySearcher
from src.models.supplier import Supplier
from src.models.juridical_entity import JuridicalEntity
import uuid

@pytest.fixture
def supplier_manager():
    json_handler = MagicMock(spec=JsonHandler)
    company_searcher = MagicMock(spec=CompanySearcher)
    supplier_manager = SupplierManager(json_handler, company_searcher)
    supplier_manager.suppliers = [] 
    return supplier_manager

def test_initialization(supplier_manager):
    supplier_manager.json_handler.load_json.assert_called_once_with(SupplierManager.FILE_PATH)

@patch('supplier_manager.get_confirmation', return_value=True)
@patch('supplier_manager.get_supplier_input_from_user', return_value=Supplier(
    entity=JuridicalEntity("Test Supplier", "Test Address", 123456789),
    bank_account="LT123456789",
    bank_name="Test Bank",
    id=str(uuid.uuid4())
))
def test_handle_add_supplier(mock_get_supplier_input, mock_get_confirmation, supplier_manager):
    new_supplier = Supplier(
        entity=JuridicalEntity("Test Supplier", "Test Address", 123456789),
        bank_account="LT123456789",
        bank_name="Test Bank",
        id=str(uuid.uuid4())
    )
    supplier_manager.json_handler.save = MagicMock()
    supplier_manager._load_suppliers_from_json = MagicMock(return_value=[new_supplier])

    supplier_manager._handle_add_supplier()

    supplier_manager.json_handler.save.assert_called_once()
    assert len(supplier_manager.suppliers) == 1
    assert supplier_manager.suppliers[0].entity.name == "Test Supplier"

@patch('supplier_manager.get_confirmation', return_value=True)
@patch('builtins.input', side_effect=["1"])
def test_handle_delete_supplier(mock_input, mock_get_confirmation, supplier_manager):
    supplier = Supplier(
        entity=JuridicalEntity("Test Supplier", "Test Address", 123456789),
        bank_account="LT123456789",
        bank_name="Test Bank",
        id=str(uuid.uuid4())
    )
    supplier_manager.suppliers = [supplier]
    supplier_manager.json_handler.delete_entry = MagicMock()

    supplier_manager._handle_delete_supplier()

    supplier_manager.json_handler.delete_entry.assert_called_once()
    assert len(supplier_manager.suppliers) == 0

@patch('builtins.input', side_effect=[""])
def test_handle_view_suppliers(mock_input, supplier_manager, capsys):
    supplier = Supplier(
        entity=JuridicalEntity("Test Supplier", "Test Address", 123456789),
        bank_account="LT123456789",
        bank_name="Test Bank",
        id=str(uuid.uuid4())
    )
    supplier_manager.suppliers = [supplier]

    supplier_manager._handle_view_suppliers()

    captured = capsys.readouterr()

    assert "Test Supplier" in captured.out
    assert "Test Address" in captured.out
    assert "123456789" in captured.out
