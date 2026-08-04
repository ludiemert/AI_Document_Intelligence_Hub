# This file exports invoice data from SQLite.
# It creates CSV and JSON reports for business use.

# This imports json from Python.
# We use json to save data for web apps and APIs.
import json

# This imports Path from Python.
# We use Path to work with folders and files.
from pathlib import Path

# This imports pandas.
# We use pandas to create CSV reports and filter data.
import pandas as pd

# This imports the repository function.
# The repository reads invoice data from SQLite.
from services.invoice_repository import load_invoices

# This is the reports folder path.
# The app saves exported reports in this folder.
REPORTS_FOLDER = Path("reports")

# This creates the reports folder if it does not exist.
REPORTS_FOLDER.mkdir(exist_ok=True)


def export_invoices_from_sqlite(selected_year="all", selected_month="all"):
    """Export invoices from SQLite using year and month filters."""
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

    # This converts invoice_date to real dates.
    # Pandas needs dates to filter by year and month.
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

    # This creates a year column from invoice_date.
    df["invoice_year"] = df["invoice_date"].dt.year.astype("Int64").astype(str)

    # This creates a month column from invoice_date.
    df["invoice_month"] = (
        df["invoice_date"].dt.month.astype("Int64").astype(str).str.zfill(2)
    )

    # This filters by selected year if the user did not choose All.
    if selected_year != "all":
        df = df[df["invoice_year"] == selected_year]

    # This filters by selected month if the user did not choose All.
    if selected_month != "all":
        df = df[df["invoice_month"] == selected_month]

    # This creates a report name using selected filters.
    # Example: invoices_2026_06
    report_name = f"invoices_{selected_year}_{selected_month}"

    # This creates the CSV file path.
    # Example: reports/invoices_2026_06.csv
    csv_file_path = REPORTS_FOLDER / f"{report_name}.csv"

    # This creates the JSON file path.
    # Example: reports/invoices_2026_06.json
    json_file_path = REPORTS_FOLDER / f"{report_name}.json"

    # This saves filtered invoice data as CSV.
    # sep=";" helps Excel open columns correctly in Europe.
    df.to_csv(csv_file_path, sep=";", index=False)

    # This saves filtered invoice data as JSON.
    with open(json_file_path, mode="w", encoding="utf-8") as json_file:
        json.dump(df.to_dict(orient="records"), json_file, indent=4, default=str)

    # This returns a success result.
    return {
        "success": True,
        "message": "Reports exported successfully.",
        "csv_file": str(csv_file_path),
        "json_file": str(json_file_path),
    }
