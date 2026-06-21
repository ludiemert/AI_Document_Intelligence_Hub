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

# This is the reports folder path.
# The app reads and saves report files in this folder.
REPORTS_FOLDER = Path("reports")

# This creates the reports folder if it does not exist.
REPORTS_FOLDER.mkdir(exist_ok=True)


def show_invoice_data(df):
    """Show invoice data in the terminal."""
    print("INVOICE DATA")
    print("------------")
    print(df)
    print()


def calculate_status_counts(df):
    """Count invoices by status."""
    # This counts invoices by status.
    status_counts = df["status"].value_counts()

    print("STATUS COUNTS")
    print("-------------")
    print(status_counts)
    print()

    return status_counts


def calculate_business_metrics(df, status_counts):
    """Calculate main business metrics."""
    # This calculates the total invoice amount.
    total_invoice_amount = df["total_amount"].sum()

    # This calculates the average risk score.
    average_risk_score = df["risk_score"].mean()

    # This rounds the average risk score to 2 decimal places.
    average_risk_score = round(average_risk_score, 2)

    # This calculates how many invoices need review.
    needs_review_count = int(status_counts.get("needs_review", 0))

    # This calculates the percentage of invoices that need review.
    needs_review_percentage = (needs_review_count / len(df)) * 100

    # This rounds the percentage to 2 decimal places.
    needs_review_percentage = round(needs_review_percentage, 2)

    print("BUSINESS METRICS")
    print("----------------")
    print(f"total_invoice_amount: {total_invoice_amount:.2f} EUR")
    print(f"average_risk_score: {average_risk_score}")

    return {
        "total_invoice_amount": float(total_invoice_amount),
        "average_risk_score": float(average_risk_score),
        "needs_review_percentage": float(needs_review_percentage),
    }


def create_recommendation(metrics):
    """Create a simple business recommendation."""
    # This gets the needs review percentage.
    needs_review_percentage = metrics["needs_review_percentage"]

    # This gets the average risk score.
    average_risk_score = metrics["average_risk_score"]

    # This creates a recommendation based on business rules.
    if needs_review_percentage > 50:
        recommendation = (
            "More than 50% of invoices need review. "
            "The finance team should check invoice quality and supplier deadlines."
        )
    elif average_risk_score > 30:
        recommendation = (
            "The average risk score is high. "
            "The company should review high-risk invoices first."
        )
    else:
        recommendation = (
            "Invoice risk is under control. "
            "The team should continue monitoring the process."
        )

    print()
    print("BUSINESS RECOMMENDATION")
    print("-----------------------")
    print(f"needs_review_percentage: {needs_review_percentage}%")
    print(f"recommendation: {recommendation}")

    return recommendation


def create_monthly_summary(df):
    """Create a monthly summary report."""
    # This groups invoices by year and month.
    monthly_summary = (
        df.groupby(["invoice_year", "invoice_month"])
        .agg(
            total_invoices=("invoice_number", "count"),
            total_invoice_amount=("total_amount", "sum"),
            average_risk_score=("risk_score", "mean"),
        )
        .reset_index()
    )

    # This rounds the average risk score to 2 decimal places.
    monthly_summary["average_risk_score"] = monthly_summary["average_risk_score"].round(
        2
    )

    print()
    print("MONTHLY SUMMARY")
    print("---------------")
    print(monthly_summary)

    return monthly_summary


def create_monthly_status_summary(df):
    """Create a monthly status summary report."""
    # This groups invoices by year, month, and status.
    monthly_status_summary = (
        df.groupby(["invoice_year", "invoice_month", "status"])
        .agg(total_invoices=("invoice_number", "count"))
        .reset_index()
    )

    print()
    print("MONTHLY STATUS SUMMARY")
    print("----------------------")
    print(monthly_status_summary)

    return monthly_status_summary


def save_monthly_reports(monthly_summary, monthly_status_summary):
    """Save monthly reports as CSV files."""
    # This is the monthly summary CSV file path.
    monthly_summary_file_name = REPORTS_FOLDER / "invoice_monthly_summary.csv"

    # This saves the monthly summary as a CSV file.
    monthly_summary.to_csv(monthly_summary_file_name, sep=";", index=False)

    print(f"Monthly summary CSV created: {monthly_summary_file_name}")

    # This is the monthly status summary CSV file path.
    monthly_status_file_name = REPORTS_FOLDER / "invoice_monthly_status_summary.csv"

    # This saves the monthly status summary as a CSV file.
    monthly_status_summary.to_csv(monthly_status_file_name, sep=";", index=False)

    print(f"Monthly status summary CSV created: {monthly_status_file_name}")


def save_summary_files(df, status_counts, metrics, recommendation):
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
    summary_file_name = REPORTS_FOLDER / "invoice_summary.csv"
    summary_df.to_csv(summary_file_name, sep=";", index=False)
    print(f"Summary CSV created: {summary_file_name}")

    # This saves the summary as a JSON file.
    summary_json_file_name = REPORTS_FOLDER / "invoice_summary.json"
    with open(summary_json_file_name, mode="w", encoding="utf-8") as json_file:
        json.dump(summary_data, json_file, indent=4)

    print(f"Summary JSON created: {summary_json_file_name}")


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
    save_monthly_reports(monthly_summary, monthly_status_summary)

    # This saves summary CSV and JSON files.
    save_summary_files(df, status_counts, metrics, recommendation)

    # This creates charts.
    create_status_chart(status_counts)
    create_risk_score_chart(df)
    create_monthly_status_chart(monthly_status_summary)


# This condition starts the program.
# It runs main() only when we run this file directly.
if __name__ == "__main__":
    main()
