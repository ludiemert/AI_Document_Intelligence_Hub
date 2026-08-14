# This file reads invoice data for the Flask app.
# Now it reads from SQLite instead of JSON.

# This imports the database connection function.
# We use it to read data from SQLite.
from services.database import get_connection


def convert_row_to_dict(row):
    """Convert SQLite row to dictionary."""
    # This converts one SQLite row into a normal Python dictionary.
    return dict(row)


def load_invoices():
    """Load all invoices from SQLite."""
    # This opens the database connection.
    connection = get_connection()

    # This creates a cursor to run SQL commands.
    cursor = connection.cursor()

    # This selects all invoices from the database.
    # source_type shows if the invoice came from TXT or OCR image.
    cursor.execute("""
        SELECT
            source_file,
            source_type,
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
        FROM invoices
        ORDER BY invoice_date ASC
        """)

    # This gets all rows from the database.
    rows = cursor.fetchall()

    # This closes the database connection.
    connection.close()

    # This converts rows into dictionaries.
    invoices = [convert_row_to_dict(row) for row in rows]

    # This returns invoice data.
    return invoices


def find_invoice_by_number(invoice_number):
    """Find one invoice by invoice number."""
    # This opens the database connection.
    connection = get_connection()

    # This creates a cursor to run SQL commands.
    cursor = connection.cursor()

    # This selects one invoice by invoice number.
    # source_type helps the detail page show where the invoice came from.
    cursor.execute(
        """
        SELECT
            source_file,
            source_type,
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
        FROM invoices
        WHERE invoice_number = ?
        """,
        (invoice_number,),
    )

    # This gets one row from the database.
    row = cursor.fetchone()

    # This closes the database connection.
    connection.close()

    # This checks if no invoice was found.
    if row is None:
        return None

    # This converts the row into a dictionary.
    return convert_row_to_dict(row)


def save_invoice(invoice):
    """Save one invoice into SQLite."""
    # This opens the database connection.
    connection = get_connection()

    # This creates a cursor to run SQL commands.
    cursor = connection.cursor()

    # This inserts or updates one invoice.
    # source_type saves if the invoice came from TXT or OCR image.
    cursor.execute(
        """
        INSERT OR REPLACE INTO invoices (
            source_file,
            source_type,
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            invoice.get("source_file"),
            invoice.get("source_type"),
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

    # This saves the database change.
    connection.commit()

    # This closes the database connection.
    connection.close()
