# This file imports invoice JSON data into SQLite.
# It reads reports/invoice_results.json and saves data in the database.

# This imports json from Python.
# We use json to read invoice data.
import json

# This imports Path from Python.
# Path helps us work with files and folders.
from pathlib import Path

# This imports database functions.
# We use them to create tables and connect to SQLite.
from services.database import create_tables, get_connection

# This is the reports folder path.
# The invoice JSON file is inside this folder.
REPORTS_FOLDER = Path("reports")


def load_invoice_json():
    """Load invoices from JSON file."""
    # This is the JSON file path.
    file_path = REPORTS_FOLDER / "invoice_results.json"

    # This opens and reads the JSON file.
    with open(file_path, mode="r", encoding="utf-8") as json_file:
        invoices = json.load(json_file)

    # This returns invoice data.
    return invoices


def save_invoice_to_database(invoice):
    """Save one invoice into SQLite."""
    # This opens the database connection.
    connection = get_connection()

    # This creates a cursor to run SQL commands.
    cursor = connection.cursor()

    # This inserts or updates one invoice.
    cursor.execute(
        """
        INSERT OR REPLACE INTO invoices (
            source_file,
            invoice_number,
            supplier_name,
            invoice_date,
            due_date,
            total_amount,
            currency,
            vat_number,
            status,
            risk_score,
            reasons
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            invoice.get("source_file"),
            invoice.get("invoice_number"),
            invoice.get("supplier_name"),
            invoice.get("invoice_date"),
            invoice.get("due_date"),
            float(invoice.get("total_amount", 0)),
            invoice.get("currency"),
            invoice.get("vat_number"),
            invoice.get("status"),
            int(invoice.get("risk_score", 0)),
            invoice.get("reasons"),
        ),
    )

    # This saves the change.
    connection.commit()

    # This closes the connection.
    connection.close()


def import_invoices_to_database():
    """Import all invoices from JSON into SQLite."""
    # This creates the table if it does not exist.
    create_tables()

    # This loads invoices from JSON.
    invoices = load_invoice_json()

    # This saves each invoice into the database.
    for invoice in invoices:
        save_invoice_to_database(invoice)

    # This shows a success message.
    print(f"{len(invoices)} invoices imported into SQLite.")


if __name__ == "__main__":
    # This runs the import process.
    import_invoices_to_database()
