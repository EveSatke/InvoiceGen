from utils.json_handler import JsonHandler
from models.invoice import Invoice
from models.item import Item
from models.juridical_entity import JuridicalEntity
from models.physical_person import PhysicalPerson
from models.supplier import Supplier


class InvoiceDataManager:
    def __init__(self, json_handler: JsonHandler, filename: str):
        self.json_handler = json_handler
        self.filename = filename

    def save_invoice(self, invoice: Invoice):
        invoice_data = invoice.to_dict()
        self.json_handler.save(self.filename, invoice_data)

    def load_invoices(self) -> list[Invoice]:
        raw_data = self.json_handler.load_json(self.filename)
        invoices = [
            Invoice(
                invoice_number=data['invoice_number'],
                invoice_date=data['invoice_date'],
                supplier=self._create_supplier(data['supplier']),
                items=[Item(**item) for item in data['items']],
                buyer=self._create_buyer(data['buyer'])
            )
            for data in raw_data
        ]
        return invoices

    def _create_buyer(self, buyer_data: dict) -> JuridicalEntity | PhysicalPerson:
        if 'registration_code' in buyer_data:
            return JuridicalEntity(**buyer_data)
        else:
            return PhysicalPerson(**buyer_data)

    def _create_supplier(self, supplier_data: dict) -> Supplier:
        entity_data = supplier_data['entity']
        entity = JuridicalEntity(
            name=entity_data['name'],
            address=entity_data['address'],
            registration_code=entity_data['registration_code'],
            vat_payer_code=entity_data.get('vat_payer_code')
        )
        return Supplier(
            entity=entity,
            bank_account=supplier_data['bank_account'],
            bank_name=supplier_data['bank_name'],
            id=supplier_data['id']
        )