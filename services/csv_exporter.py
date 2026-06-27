# This imports json from Python.
# We use json to save data for web dashboards.
import json

# This imports csv from Python.
# We use csv to save invoice results in a table file.
import csv

# This imports Path from Python.
# We use Path to work with folder and file paths.
from pathlib import Path

# This is the reports folder path.
# The app saves output files in this folder.
REPORTS_FOLDER = Path("reports")
# This creates the reports folder if it does not exist.
REPORTS_FOLDER.mkdir(exist_ok=True)


# This function saves processed invoices in a CSV file.
# CSV is a table file that Excel and Pandas can read.
def save_results_to_csv(results):
    """Save processed invoice results to a CSV file."""
    # This is the CSV file path inside the reports folder.
    file_name = REPORTS_FOLDER / "invoice_results.csv"

    # These are the CSV column names.
    fieldnames = [
        "source_file",
        "invoice_number",
        "supplier_name",
        "invoice_date",
        "due_date",
        "total_amount",
        "currency",
        "status",
        "risk_score",
        "reasons",
    ]

    # This opens the CSV file in write mode.
    # newline="" helps avoid blank lines in Windows.
    with open(file_name, mode="w", newline="", encoding="utf-8") as csv_file:
        # This creates a CSV writer that uses dictionary keys.
        # delimiter=";" helps Excel open columns correctly in Europe.
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

        # This writes the first row with column names.
        writer.writeheader()

        # This writes all processed invoice rows.
        writer.writerows(results)

    # This message tells the user the CSV was created.
    print(f"CSV file created: {file_name}")

    # This is the JSON file path inside the reports folder.
    json_file_name = REPORTS_FOLDER / "invoice_results.json"

    # This opens the JSON file in write mode.
    # encoding="utf-8" helps save text correctly.
    with open(json_file_name, mode="w", encoding="utf-8") as json_file:
        # This saves processed invoices as JSON.
        # indent=4 makes the JSON easy to read.
        json.dump(results, json_file, indent=4)

    # This message tells the user the JSON was created.
    print(f"JSON file created: {json_file_name}")
