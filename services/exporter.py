# This file exports invoice data from SQLite.
# It creates CSV and JSON reports for business use.

# This imports json from Python.
# We use json to save data for web apps and APIs.
import json

# This imports Path from Python.
# We use Path to work with folders and files.
from pathlib import Path

# This imports pandas.
# We use pandas to create CSV reports.
import pandas as pd

# This imports the repository function.
# The repository reads invoice data from SQLite.
from services.invoice_repository import load_invoices

# This is the reports folder path.
# The app saves exported reports in this folder.
REPORTS_FOLDER = Path("reports")

# This creates the reports folder if it does not exist.
REPORTS_FOLDER.mkdir(exist_ok=True)


def export_invoices_from_sqlite():
    """Export invoices from SQLite to CSV and JSON."""
    # This loads invoice data from SQLite.
    invoices = load_invoices()

    # This checks if there are no invoices.
    if not invoices:
        return {
            "success": False,
            "message": "No invoices found to export.",
        }

    # This creates a DataFrame from invoice data.
    df = pd.DataFrame(invoices)

    # This creates the CSV file path.
    csv_file_path = REPORTS_FOLDER / "sqlite_invoice_export.csv"

    # This saves invoice data as CSV.
    # sep=";" helps Excel open columns correctly in Europe.
    df.to_csv(csv_file_path, sep=";", index=False)

    # This creates the JSON file path.
    json_file_path = REPORTS_FOLDER / "sqlite_invoice_export.json"

    # This saves invoice data as JSON.
    with open(json_file_path, mode="w", encoding="utf-8") as json_file:
        json.dump(invoices, json_file, indent=4)

    # This returns a success result.
    return {
        "success": True,
        "message": "Reports exported successfully.",
        "csv_file": str(csv_file_path),
        "json_file": str(json_file_path),
    }
