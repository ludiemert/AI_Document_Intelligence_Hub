# This file controls the SQLite database.
# SQLite saves invoice data in a real database file.

# This imports sqlite3 from Python.
# We use sqlite3 to create and use the database.
import sqlite3

# This imports Path from Python.
# Path helps us work with folders and files.
from pathlib import Path

# This is the data folder path.
# The database file will stay inside this folder.
DATA_FOLDER = Path("data")

# This creates the data folder if it does not exist.
DATA_FOLDER.mkdir(exist_ok=True)

# This is the SQLite database file path.
DATABASE_FILE = DATA_FOLDER / "invoices.db"


def get_connection():
    """Create a database connection."""
    # This connects Python to the SQLite database.
    connection = sqlite3.connect(DATABASE_FILE)

    # This makes rows work like dictionaries.
    connection.row_factory = sqlite3.Row

    # This returns the database connection.
    return connection


def create_tables():
    """Create database tables."""
    # This opens the database connection.
    connection = get_connection()

    # This creates a cursor to run SQL commands.
    cursor = connection.cursor()

    # This creates the invoices table if it does not exist.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT,
            invoice_number TEXT UNIQUE,
            supplier_name TEXT,
            invoice_date TEXT,
            due_date TEXT,
            total_amount REAL,
            currency TEXT,
            vat_number TEXT,
            status TEXT,
            risk_score INTEGER,
            reasons TEXT
        )
        """)

    # This saves the database changes.
    connection.commit()

    # This closes the database connection.
    connection.close()


if __name__ == "__main__":
    # This creates the database table when we run this file.
    create_tables()

    # This shows a success message.
    print("Database and invoices table created.")
