# This file reads invoice data for the Flask app.
# Later, this file can read from SQLite instead of JSON.

# This imports json from Python.
# We use json to read invoice data.
import json

# This imports Path from Python.
# Path helps us work with files and folders.
from pathlib import Path

# This is the reports folder path.
# The invoice JSON file is inside this folder.
REPORTS_FOLDER = Path("reports")


def load_invoices():
    """Load all invoices from JSON."""
    # This is the invoice JSON file path.
    file_path = REPORTS_FOLDER / "invoice_results.json"

    # This opens the JSON file.
    with open(file_path, mode="r", encoding="utf-8") as json_file:
        invoices = json.load(json_file)

    # This returns all invoices.
    return invoices


def find_invoice_by_number(invoice_number):
    """Find one invoice by invoice number."""
    # This loads all invoices.
    invoices = load_invoices()

    # This checks each invoice.
    for invoice in invoices:
        # This compares the invoice number.
        if invoice["invoice_number"] == invoice_number:
            return invoice

    # This returns nothing if invoice was not found.
    return None
