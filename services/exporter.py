# This file exports invoice data from SQLite.
# It creates CSV and JSON reports for business use.

# This imports json from Python.
# We use json to save data for web apps and APIs.
import json

# This imports Path from Python.
# We use Path to work with folders and files.
from pathlib import Path

# This imports pandas.
# We use pandas to create business reports.
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

    # This converts total_amount to number.
    # Reports need numbers for sums and averages.
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)

    # This converts risk_score to number.
    # Reports need numbers for risk calculations.
    df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(0)

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

    # This checks if the selected filters found no data.
    if df.empty:
        return {
            "success": False,
            "message": "No invoices found for the selected filters.",
        }

    # This creates a report name using selected filters.
    # Example: invoices_2026_06
    report_name = f"invoices_{selected_year}_{selected_month}"

    # This creates the detailed CSV file path.
    detailed_csv_file_path = REPORTS_FOLDER / f"{report_name}.csv"

    # This creates the detailed JSON file path.
    detailed_json_file_path = REPORTS_FOLDER / f"{report_name}.json"

    # This saves filtered invoice data as CSV.
    # sep=";" helps Excel open columns correctly in Europe.
    df.to_csv(detailed_csv_file_path, sep=";", index=False)

    # This saves filtered invoice data as JSON.
    with open(detailed_json_file_path, mode="w", encoding="utf-8") as json_file:
        json.dump(df.to_dict(orient="records"), json_file, indent=4, default=str)

    # This creates the monthly summary report.
    # It groups invoices by year and month.
    monthly_summary = (
        df.groupby(["invoice_year", "invoice_month"])
        .agg(
            total_invoices=("invoice_number", "count"),
            total_invoice_amount=("total_amount", "sum"),
            average_risk_score=("risk_score", "mean"),
        )
        .reset_index()
    )

    # This rounds monthly numbers to 2 decimals.
    monthly_summary["total_invoice_amount"] = monthly_summary[
        "total_invoice_amount"
    ].round(2)
    monthly_summary["average_risk_score"] = monthly_summary["average_risk_score"].round(
        2
    )

    # This creates the monthly summary CSV file path.
    monthly_summary_file_path = (
        REPORTS_FOLDER / f"monthly_summary_{selected_year}_{selected_month}.csv"
    )

    # This saves the monthly summary as CSV.
    monthly_summary.to_csv(monthly_summary_file_path, sep=";", index=False)

    # This creates the yearly summary report.
    # It groups invoices by year.
    yearly_summary = (
        df.groupby("invoice_year")
        .agg(
            total_invoices=("invoice_number", "count"),
            total_invoice_amount=("total_amount", "sum"),
            average_risk_score=("risk_score", "mean"),
        )
        .reset_index()
    )

    # This counts invoice status by year.
    yearly_status_summary = df.pivot_table(
        index="invoice_year",
        columns="status",
        values="invoice_number",
        aggfunc="count",
        fill_value=0,
    ).reset_index()

    # This makes sure all status columns exist.
    # Some filters may not have approved, needs_review, or high_risk.
    for status_name in ["approved", "needs_review", "high_risk"]:
        if status_name not in yearly_status_summary.columns:
            yearly_status_summary[status_name] = 0

    # This joins yearly metrics with yearly status counts.
    yearly_summary = yearly_summary.merge(
        yearly_status_summary[
            ["invoice_year", "approved", "needs_review", "high_risk"]
        ],
        on="invoice_year",
        how="left",
    )

    # This rounds yearly numbers to 2 decimals.
    yearly_summary["total_invoice_amount"] = yearly_summary[
        "total_invoice_amount"
    ].round(2)
    yearly_summary["average_risk_score"] = yearly_summary["average_risk_score"].round(2)

    # This creates the yearly summary CSV file path.
    yearly_summary_file_path = (
        REPORTS_FOLDER / f"yearly_summary_{selected_year}_{selected_month}.csv"
    )

    # This saves the yearly summary as CSV.
    yearly_summary.to_csv(yearly_summary_file_path, sep=";", index=False)

    # This creates the risk summary report.
    # It groups invoices by status.
    risk_summary = (
        df.groupby("status")
        .agg(
            total_invoices=("invoice_number", "count"),
            average_invoice_amount=("total_amount", "mean"),
            average_risk_score=("risk_score", "mean"),
        )
        .reset_index()
    )

    # This rounds risk summary numbers to 2 decimals.
    risk_summary["average_invoice_amount"] = risk_summary[
        "average_invoice_amount"
    ].round(2)
    risk_summary["average_risk_score"] = risk_summary["average_risk_score"].round(2)

    # This creates the risk summary CSV file path.
    risk_summary_file_path = (
        REPORTS_FOLDER / f"risk_summary_{selected_year}_{selected_month}.csv"
    )

    # This saves the risk summary as CSV.
    risk_summary.to_csv(risk_summary_file_path, sep=";", index=False)

    # This returns a success result.
    return {
        "success": True,
        "message": "Reports exported successfully.",
        "csv_file": str(detailed_csv_file_path),
        "json_file": str(detailed_json_file_path),
        "monthly_summary_file": str(monthly_summary_file_path),
        "yearly_summary_file": str(yearly_summary_file_path),
        "risk_summary_file": str(risk_summary_file_path),
    }
