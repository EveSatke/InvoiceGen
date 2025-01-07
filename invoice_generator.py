from colorama import Fore
from weasyprint import HTML
from models.invoice import Invoice
import os
from models.juridical_entity import JuridicalEntity
from datetime import datetime


class InvoiceGenerator:
    def __init__(self, base_directory: str):
        self.base_directory = base_directory

    def generate_invoice_pdf(self, invoice: Invoice):
        try:
            supplier_name = invoice.supplier.entity.name
            supplier_directory = os.path.join(self.base_directory, supplier_name)

            # Create directory for the supplier if it doesn't exist
            os.makedirs(supplier_directory, exist_ok=True)

            # Define the filename using the invoice number
            invoice_date = datetime.now().strftime("%Y-%m-%d")
            filename = f"Saskaita_{invoice.invoice_number}_{invoice_date}.pdf"
            file_path = os.path.join(supplier_directory, filename)

            # Generate the PDF
            supplier_vat_code = invoice.supplier.entity.vat_payer_code
            buyer_vat_code = getattr(invoice.buyer, 'vat_payer_code', None)
            buyer_registration_code = getattr(invoice.buyer, 'registration_code', None)
            buyer_surname = getattr(invoice.buyer, 'surname', None)

            html_content = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        font-size: 14px;
                        margin: 0;
                        padding: 0;
                        color: #333;
                        width: 100%;
                        height: auto;
                        display: flex;
                        justify-content: center;
                        align-items: flex-start;
                        background: #fff
                        
                    }}
                    .invoice-box {{
                        width: 800px;
                        height: 980px;
                        padding: 20px;
                        background: #fff;
                        box-sizing: border-box;
                        overflow: hidden;
                        border: 1px solid #ddd;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        box-sizing: border-box;
                    }}
                    .invoice-header {{
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 40px;
                    }}
                    .invoice-header .title {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #333;
                    }}
                    .invoice-header .details {{
                        text-align: right;
                    }}
                    .invoice-section {{
                        margin-bottom: 20px;
                        display: flex;
                        justify-content: space-between;
                    }}
                    .invoice-section .section-title {{
                        font-weight: bold;
                        margin-bottom: 5px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }}
                    table, th, td {{
                        border: 1px solid #ddd;
                    }}
                    th, td {{
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f2f2f2;
                        font-weight: bold;
                    }}
                    .total-row {{
                        font-weight: bold;
                        text-align: right;
                    }}
                    .total-row td {{
                        border-top: 2px solid #ddd;
                    }}
                    .total-row-title {{
                        text-align: right;
                        padding-right: 8px;
                    }}
                    .sum-in-words {{
                        margin-top: 10px;
                        font-style: italic;
                        font-size: 13px;
                    }}
                </style>
            </head>
            <body>
                <div class="invoice-box">
                    <div class="invoice-header">
                        <div class="title">{"PVM sąskaita - faktūra" if supplier_vat_code else "Sąskaita - faktūra"}</div>
                        <div class="details">
                            Sąskaitos Nr.: {invoice.invoice_number}<br>
                            Data: {invoice.invoice_date}
                        </div>
                    </div>

                    <div class="invoice-section">
                        <div>
                            <div class="section-title">Tiekėjas:</div>
                            {invoice.supplier.entity.name}<br>
                            {invoice.supplier.entity.address}<br>
                            Įmonės kodas: {invoice.supplier.entity.registration_code if isinstance(invoice.supplier.entity, JuridicalEntity) else ""}<br>
                            Sąskaitos numeris: {invoice.supplier.bank_account}<br>
                            Bankas: {invoice.supplier.bank_name}<br>
                            {"PVM kodas: " + supplier_vat_code if supplier_vat_code else ""}<br>
                        </div>
                        <div class="buyer-details">
                            <div class="section-title">Pirkėjas:</div>
                            {invoice.buyer.name} {buyer_surname if buyer_surname else ""}<br>
                            {invoice.buyer.address}<br>
                            {f"Įmonės kodas: {buyer_registration_code}<br>" if buyer_registration_code else ""}
                            {f"PVM kodas: {buyer_vat_code}<br>" if buyer_vat_code else ""}
                        </div>
                    </div>

                    <table>
                        <tr>
                            <th>Aprašymas</th>
                            <th>Kiekis</th>
                            <th>Vieneto kaina</th>
                            <th>Suma</th>
                        </tr>
                        {"".join(f"""
                        <tr>
                            <td>{item.name}</td>
                            <td>{item.quantity}</td>
                            <td>{item.price:.2f} EUR</td>
                            <td>{item.price * item.quantity:.2f} EUR</td>
                        </tr>
                        """ for item in invoice.items)}
                        {f"""
                        <tr class="total-row">
                            <td colspan="3" class="total-row-title">PVM suma:</td>
                            <td>{invoice.total_vat:.2f} EUR</td>
                        </tr>
                        """ if supplier_vat_code else ""}
                        <tr class="total-row">
                            <td colspan="3" class="total-row-title">Iš viso:</td>
                            <td>{invoice.total_amount:.2f} EUR</td>
                        </tr>
                    </table>

                    <div class="sum-in-words">
                        Suma žodžiais: {invoice.sum_in_words}.
                    </div>
                </div>
            </body>
            </html>
            """
            HTML(string=html_content).write_pdf(file_path)
            print(f"{Fore.GREEN}\nInvoice created successfully at {file_path}.{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}\nAn error occurred while creating the invoice: {e}{Fore.RESET}")