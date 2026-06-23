# This file saves report outputs.
# It exports summary data to CSV and JSON files.

# This imports json from Python.
# We use json to save data for web apps and APIs.
import json

# This imports pandas.
# We use pandas to create summary DataFrames.
import pandas as pd


# This function saves monthly reports as CSV files.
# It saves monthly summary and monthly status summary.
def save_monthly_reports(reports_folder, monthly_summary, monthly_status_summary):
    """Save monthly reports as CSV files."""
    # This is the monthly summary CSV file path.
    monthly_summary_file_name = reports_folder / "invoice_monthly_summary.csv"

    # This saves the monthly summary as a CSV file.
    # sep=";" helps Excel open columns correctly in Europe.
    monthly_summary.to_csv(monthly_summary_file_name, sep=";", index=False)

    print(f"Monthly summary CSV created: {monthly_summary_file_name}")

    # This is the monthly status summary CSV file path.
    monthly_status_file_name = reports_folder / "invoice_monthly_status_summary.csv"

    # This saves the monthly status summary as a CSV file.
    # sep=";" helps Excel open columns correctly in Europe.
    monthly_status_summary.to_csv(monthly_status_file_name, sep=";", index=False)

    print(f"Monthly status summary CSV created: {monthly_status_file_name}")


# This function saves general summary as CSV and JSON.
# CSV is good for tables. JSON is good for web apps.
def save_summary_files(reports_folder, df, status_counts, metrics, recommendation):
    """Save general summary as CSV and JSON."""
    # This dictionary saves the business metrics.
    summary_data = {
        "total_invoices": int(len(df)),
        "approved": int(status_counts.get("approved", 0)),
        "needs_review": int(status_counts.get("needs_review", 0)),
        "high_risk": int(status_counts.get("high_risk", 0)),
        "average_risk_score": float(metrics["average_risk_score"]),
        "total_invoice_amount": float(metrics["total_invoice_amount"]),
        "needs_review_percentage": float(metrics["needs_review_percentage"]),
        "recommendation": recommendation,
        "currency": "EUR",
    }

    # This converts the summary dictionary into a DataFrame.
    summary_df = pd.DataFrame([summary_data])

    # This saves the summary as a CSV file.
    summary_file_name = reports_folder / "invoice_summary.csv"
    summary_df.to_csv(summary_file_name, sep=";", index=False)
    print(f"Summary CSV created: {summary_file_name}")

    # This saves the summary as a JSON file.
    summary_json_file_name = reports_folder / "invoice_summary.json"
    with open(summary_json_file_name, mode="w", encoding="utf-8") as json_file:
        json.dump(summary_data, json_file, indent=4)

    print(f"Summary JSON created: {summary_json_file_name}")


# This function saves invoice results separated by year.
# It creates one CSV file for each invoice year.
def save_yearly_invoice_results(reports_folder, df):
    """Save invoice results in one CSV file per year."""
    # This creates the yearly reports folder.
    yearly_folder = reports_folder / "yearly"

    # This creates the folder if it does not exist.
    yearly_folder.mkdir(exist_ok=True)

    # This gets all unique invoice years from the DataFrame.
    invoice_years = df["invoice_year"].unique()

    # This loop creates one CSV file for each year.
    for invoice_year in invoice_years:
        # This filters invoices for one year.
        yearly_df = df[df["invoice_year"] == invoice_year]

        # This creates a folder for the year.
        year_folder = yearly_folder / str(invoice_year)
        year_folder.mkdir(exist_ok=True)

        # This creates the yearly CSV file path.
        yearly_file_name = year_folder / f"invoice_results_{invoice_year}.csv"

        # This saves the year invoices as a CSV file.
        # sep=";" helps Excel open columns correctly in Europe.
        yearly_df.to_csv(yearly_file_name, sep=";", index=False)

        # This message tells the user the yearly CSV was created.
        print(f"Yearly CSV created: {yearly_file_name}")
