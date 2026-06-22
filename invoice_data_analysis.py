# This imports json from Python.
# We use json to save data for web apps and APIs.
import json

# This imports Path from Python.
# We use Path to work with folder and file paths.
from pathlib import Path

# This imports matplotlib.
# We use matplotlib to create charts.
import matplotlib.pyplot as plt

# This imports pandas.
# We use pandas to read and analyze CSV files.
import pandas as pd

# This imports data loading functions.
from services.analysis_loader import add_date_columns, load_invoice_data

# This imports summary functions.
from services.summaries import create_monthly_status_summary, create_monthly_summary

# This imports report exporter functions.
from services.report_exporter import save_monthly_reports, save_summary_files

# This imports recommendation functions.
from services.recommendations import create_recommendation

# This imports analytics functions.
from services.analytics import (
    calculate_business_metrics,
    calculate_status_counts,
    show_invoice_data,
)


def create_status_chart(status_counts):
    """Create a chart with invoice status counts."""
    # This creates a bar chart with invoice status counts.
    status_counts.plot(kind="bar")

    plt.title("Invoice Status Counts")
    plt.xlabel("Status")
    plt.ylabel("Number of Invoices")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(REPORTS_FOLDER / "status_counts.png")
    plt.clf()

    print("Chart created: status_counts.png")


def create_risk_score_chart(df):
    """Create a chart with risk score by invoice."""
    # This creates a bar chart with risk score by invoice.
    plt.bar(df["invoice_number"], df["risk_score"], color="steelblue")

    plt.title("Risk Score by Invoice")
    plt.xlabel("Invoice Number")
    plt.ylabel("Risk Score")
    plt.tight_layout()
    plt.savefig(REPORTS_FOLDER / "risk_scores.png")
    plt.clf()

    print("Chart created: risk_scores.png")


# This is the reports folder path.
# The app reads and saves report files in this folder.
REPORTS_FOLDER = Path("reports")

# This creates the reports folder if it does not exist.
REPORTS_FOLDER.mkdir(exist_ok=True)


def create_monthly_status_chart(monthly_status_summary):
    """Create a chart with monthly status counts."""
    # This changes rows into columns for the chart.
    monthly_status_chart = monthly_status_summary.pivot_table(
        index=["invoice_year", "invoice_month"],
        columns="status",
        values="total_invoices",
        fill_value=0,
    )

    # This creates a bar chart from the monthly status table.
    monthly_status_chart.plot(kind="bar")

    plt.title("Monthly Invoice Status Counts")
    plt.xlabel("Year and Month")
    plt.ylabel("Number of Invoices")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(REPORTS_FOLDER / "monthly_status_counts.png")
    plt.clf()

    print("Chart created: monthly_status_counts.png")


def main():
    """Run the invoice data analysis workflow."""
    # This loads the invoice data from CSV.
    df = load_invoice_data()

    # This adds year and month columns.
    df = add_date_columns(df)

    # This shows the invoice data.
    show_invoice_data(df)

    # This calculates status counts.
    status_counts = calculate_status_counts(df)

    # This calculates business metrics.
    metrics = calculate_business_metrics(df, status_counts)

    # This creates a business recommendation.
    recommendation = create_recommendation(metrics)

    # This creates monthly reports.
    monthly_summary = create_monthly_summary(df)
    monthly_status_summary = create_monthly_status_summary(df)

    # This saves monthly reports.
    save_monthly_reports(REPORTS_FOLDER, monthly_summary, monthly_status_summary)

    # This saves summary CSV and JSON files.
    save_summary_files(REPORTS_FOLDER, df, status_counts, metrics, recommendation)

    # This creates charts.
    create_status_chart(status_counts)
    create_risk_score_chart(df)
    create_monthly_status_chart(monthly_status_summary)


# This condition starts the program.
# It runs main() only when we run this file directly.
if __name__ == "__main__":
    main()
