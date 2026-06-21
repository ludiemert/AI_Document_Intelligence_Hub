# This imports Path from Python.
# We use Path to work with folder and file paths.
from pathlib import Path

# This imports pandas.
# We use pandas to read and analyze CSV files.
import pandas as pd

# This is the reports folder path.
# The app reads report files from this folder.
REPORTS_FOLDER = Path("reports")

# This creates the reports folder if it does not exist.
REPORTS_FOLDER.mkdir(exist_ok=True)


# This function loads invoice results from CSV.
# It returns a DataFrame with invoice data.
def load_invoice_data():
    """Load invoice results from CSV."""
    # This is the CSV file created by invoice_analyzer.py.
    file_name = REPORTS_FOLDER / "invoice_results.csv"

    # This reads the CSV file and creates a DataFrame.
    # sep=";" means the CSV uses semicolon as separator.
    df = pd.read_csv(file_name, sep=";")

    # This returns the invoice table.
    return df


# This function adds year and month columns.
# It helps create monthly and yearly reports.
def add_date_columns(df):
    """Add year and month columns to the invoice data."""
    # This converts invoice_date from text to date.
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])

    # This creates a new column with the invoice year.
    df["invoice_year"] = df["invoice_date"].dt.year

    # This creates a new column with the invoice month.
    df["invoice_month"] = df["invoice_date"].dt.month

    # This returns the updated DataFrame.
    return df
