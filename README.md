# InvoiceGen

InvoiceGen is a Python-based application designed to manage and generate invoices for suppliers and buyers. It provides functionalities to add, view invoices and manage supplier profiles.

## Features

- **Invoice Generation**: Create detailed invoices with supplier and buyer information.
- **Supplier Management**: Add, view, and delete supplier profiles.
- **Invoice Viewing**: View all generated invoices in a tabulated format.
- **Data Persistence**: Store invoices and supplier data in JSON format for easy retrieval and management.

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd InvoiceGen
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   The application is started by executing the `main.py` file, which initializes the necessary components and launches the main menu.

   ```bash
   python main.py
   ```

2. **Main Menu**:

   - Add a new invoice
   - View all invoices
   - Manage supplier profiles
   - Exit the application

3. **Invoice Generation**:
   - Select a supplier from the list or add a new one.
   - Choose the buyer type (Juridical entity or Physical person).
   - Add items to the invoice with descriptions, quantities, and prices.
   - Confirm and generate the invoice.

## File Structure

- `main.py`: Entry point of the application.
- `setup.py`: Handles initial setup and data downloading.
- `invoice_generator.py`: Contains logic for generating invoice PDFs.
- `supplier_manager.py`: Manages supplier profiles.
- `invoice_manager.py`: Manages invoice creation and viewing.
- `data/`: Directory containing JSON files for invoices and suppliers.
- `models/`: Contains data models for entities like `Invoice`, `Supplier`, etc.
- `utils/`: Utility functions and helpers.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
