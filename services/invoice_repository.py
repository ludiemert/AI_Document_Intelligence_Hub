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
    cursor.execute(
        """
        SELECT
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
        FROM invoices
        ORDER BY invoice_date ASC
        """
    )

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
    cursor.execute(
        """
        SELECT
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