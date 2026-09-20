# Retail Point of Sale Backend API

This repository contains the backend API for a retail-focused Point of Sale (POS) application optimized for desktop and responsive mobile environments. The system automates inventory tracking, checkout management, customer relationship recording, and payment transaction logging for small to medium-sized retail businesses.

## System Features

- Role-Based Authentication: Route security managed through OAuth2 Password Bearer implementation and JSON Web Tokens (JWT).
- Inventory Controls: Real-time product inventory adjustment, categorization, and tracking of supplier relationships.
- Checkout Processing: Transaction management handling calculations via the Python Decimal library to eliminate floating-point rounding discrepancies.
- Split Payments: Functional tracking allowing single sales invoices to be settled across multiple distinct ledger records.
- Loyalty Tracking: Automated balance accumulation for customers linked to completed invoices.

## System Architecture

The codebase separates technical concerns by implementing a strict Router-Service-Repository pattern:

- core: Holds runtime configuration definitions, environment variable parsers, and route guard dependencies.
- models: Houses SQLAlchemy structure schemas defining database tables, constraint attributes, and data relationships.
- repository: Contains isolated database queries and basic CRUD operations.
- schemas: Employs Pydantic v2 classes to declare request inputs validation filters and response formats.
- services: Implements central business logic constraints and data transformation workflows.
- routers: Exposes individual HTTP operational route handlers grouped by table domain paths.

## Database Model and Relationships

The persistent storage layers are mapped through the following database entities:

| Entity Name | Primary Purpose                             | Structural Attributes                       |
| :---------- | :------------------------------------------ | :------------------------------------------ |
| User        | Handles credentials and security parameters | id, username, masked_password, role         |
| Customer    | Stores profiles and tracking values         | id, first_name, last_name, loyalty_points   |
| Supplier    | Contains provider address details           | id, company_name, phone, email              |
| Category    | Groups items by organizational groups       | id, name, description, created_at           |
| Product     | Maintains inventory quantities and values   | id, barcode, price, cost_price, stock_qty   |
| Sale        | Acts as the main invoice record header      | id, sale_date, total_amount, final_amount   |
| Sale Item   | Details individual line items on an invoice | id, sale_id, product_id, quantity, subtotal |
| Payment     | Records settlement ledger entries           | id, sale_id, payment_method, amount_paid    |
| Receipt     | Holds transaction document values           | id, sale_id, receipt_number, issued_at      |

### Table Relationship Mappings

- Category to Product (One-to-Many): A category holds multiple products; a product belongs to a single category.
- Supplier to Product (One-to-Many): A supplier distributes multiple products; a product links to a single supplier.
- Customer to Sale (One-to-Many): A customer initiates multiple sales; a sale maps to a single customer profile.
- User to Sale (One-to-Many): An employee processes multiple sales; a sale logs the single active user account.
- Sale to Sale Item (One-to-Many): A sale invoice includes multiple line items; a line item references a single sale header.
- Product to Sale Item (One-to-Many): A product can appear on multiple sale item lines; a line item references a single product identifier.
- Sale to Payment (One-to-Many): A sale invoice accepts multiple payment records; a payment targets a single sale.
- Sale to Receipt (One-to-One): A sale maps exclusively to a single unique receipt record document.

## Installation and Startup Execution

1. Configure environment variables by creating a configuration file named `.env` in the root folder of the project directory:

```ini
DATABASE_URL=postgresql://user:password@localhost:5432/pos_database
JWT_SECRET_KEY=e8c8942b0f343a4115e47852f86236b281b9b5f9226e107c1341c305a420cf67
```

2. Activate the local virtual environment and install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize the application worker thread using the development hot-reload loop:

```bash
fastapi dev
```

The application server will listen for requests on port 8000.

**Running tests (local)**

- Activate the virtualenv: `source env/bin/activate` (or use your preferred venv)
- Install dependencies: `pip install -r requirements.txt`
- Run the full test suite: `pytest -q` or `./env/bin/python -m pytest -q`

Tests use a temporary in-memory SQLite database and will not affect your development Postgres database.

## Interactive API Route Testing

1. Open a browser window and navigate to the integrated OpenAPI interface page at http://127.0.0
2. Execute the local setup script via the terminal interface to generate an active testing profile account.
3. Click the Authorize button located at the upper right of the documentation interface window.
4. Input the generated credential parameters into the authorization form fields, then select the Authorize confirmation control.
5. Close the form. Subsequent API endpoint operations executed through the webpage will carry the authentication header.
