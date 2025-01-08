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
- `src/data/`: Directory containing JSON files for invoices and suppliers.
- `src/models/`: Contains data models for entities like `Invoice`, `Supplier`, etc.
- `src/utils/`: Utility functions and helpers.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Testing

### Running Tests

1. **Setup**:

   - Ensure you have pytest installed:
     ```bash
     pip install pytest
     ```
   - Make sure you're in the project root directory

2. **Run All Tests**:

   ```bash
   PYTHONPATH=$PYTHONPATH:$(pwd)/src pytest tests -v
   ```

3. **Run Specific Test File**:

   ```bash
   PYTHONPATH=$PYTHONPATH:$(pwd)/src pytest tests/test_invoice_manager.py -v
   ```

4. **Test Files**:
   - `tests/test_invoice_manager.py`: Tests for invoice generation and management
   - `tests/test_supplier_manager.py`: Tests for supplier management
   - `tests/test_invoice_data_manager.py`: Tests for invoice data handling

### Test Configuration

The project uses the following test configuration:

- `pytest.ini`: Configures the Python path for tests
- `tests/conftest.py`: Contains pytest fixtures and setup
- All test files are located in the `tests/` directory
