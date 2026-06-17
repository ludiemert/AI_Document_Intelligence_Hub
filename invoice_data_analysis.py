# This imports json from Python.
# We use json to save data for web apps and APIs.
import json

# This project analyzes invoice results with Pandas.
# Pandas helps us work with table data.
# This imports pandas.
# We use pandas to read and analyze CSV files.
import pandas as pd

# This imports matplotlib.
# We use matplotlib to create charts.
import matplotlib.pyplot as plt

# This imports Path from Python.
# We use Path to work with folder and file paths.
from pathlib import Path

# This is the reports folder path.
# The app reads and saves report files in this folder.
REPORTS_FOLDER = Path("reports")

# This creates the reports folder if it does not exist.
REPORTS_FOLDER.mkdir(exist_ok=True)

# This is the CSV file created by invoice_analyzer.py.
file_name = REPORTS_FOLDER / "invoice_results.csv"

# This reads the CSV file and creates a DataFrame.
# sep=";" means the CSV uses semicolon as separator.
df = pd.read_csv(file_name, sep=";")

# This converts invoice_date from text to date.
# Dates help us create year and month reports.
df["invoice_date"] = pd.to_datetime(df["invoice_date"])

# This creates a new column with the invoice year.
# Example: 2026-06-01 becomes 2026.
df["invoice_year"] = df["invoice_date"].dt.year

# This creates a new column with the invoice month.
# Example: 2026-06-01 becomes 6.
df["invoice_month"] = df["invoice_date"].dt.month

# This shows all invoice data in the terminal.
print("INVOICE DATA")
print("------------")
print(df)

# This creates a blank line in the terminal.
print()

# This counts invoices by status.
# Example: approved, needs_review, high_risk.
status_counts = df["status"].value_counts()

print("STATUS COUNTS")
print("-------------")
print(status_counts)

# This creates a blank line in the terminal.
print()

# This calculates the total invoice amount.
total_invoice_amount = df["total_amount"].sum()

# This calculates the average risk score.
average_risk_score = df["risk_score"].mean()

# This rounds the average risk score to 2 decimal places.
average_risk_score = round(average_risk_score, 2)

print("BUSINESS METRICS")
print("----------------")
print(f"total_invoice_amount: {total_invoice_amount:.2f} EUR")
print(f"average_risk_score: {average_risk_score}")

# This creates a monthly summary.
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

# This rounds the average risk score to 2 decimal places.
monthly_summary["average_risk_score"] = monthly_summary["average_risk_score"].round(2)

print()
print("MONTHLY SUMMARY")
print("---------------")
print(monthly_summary)

# This is the monthly summary CSV file path.
monthly_summary_file_name = REPORTS_FOLDER / "invoice_monthly_summary.csv"

# This saves the monthly summary as a CSV file.
# sep=";" helps Excel open columns correctly in Europe.
monthly_summary.to_csv(monthly_summary_file_name, sep=";", index=False)

# This message tells the user the monthly summary CSV was created.
print(f"Monthly summary CSV created: {monthly_summary_file_name}")

# This creates a monthly status summary.
# It groups invoices by year, month, and status.
monthly_status_summary = (
    df.groupby(["invoice_year", "invoice_month", "status"])
    .agg(total_invoices=("invoice_number", "count"))
    .reset_index()
)

print()
print("MONTHLY STATUS SUMMARY")
print("----------------------")
print(monthly_status_summary)

# This is the monthly status summary CSV file path.
monthly_status_file_name = REPORTS_FOLDER / "invoice_monthly_status_summary.csv"

# This saves the monthly status summary as a CSV file.
# sep=";" helps Excel open columns correctly in Europe.
monthly_status_summary.to_csv(monthly_status_file_name, sep=";", index=False)

# This message tells the user the monthly status summary CSV was created.
print(f"Monthly status summary CSV created: {monthly_status_file_name}")


# This dictionary saves the business metrics.
# We convert Pandas numbers to normal Python numbers.
summary_data = {
    "total_invoices": int(len(df)),
    "approved": int(status_counts.get("approved", 0)),
    "needs_review": int(status_counts.get("needs_review", 0)),
    "high_risk": int(status_counts.get("high_risk", 0)),
    "average_risk_score": float(average_risk_score),
    "total_invoice_amount": float(total_invoice_amount),
    "currency": "EUR",
}

# This converts the summary dictionary into a DataFrame.
# Pandas needs a list to create one row.
summary_df = pd.DataFrame([summary_data])

# This is the summary CSV file path.
summary_file_name = REPORTS_FOLDER / "invoice_summary.csv"

# This saves the summary DataFrame as a CSV file.
# sep=";" helps Excel open columns correctly in Europe.
# index=False avoids an extra number column.
summary_df.to_csv(summary_file_name, sep=";", index=False)

# This message tells the user the summary CSV was created.
print(f"Summary CSV created: {summary_file_name}")

# This is the summary JSON file path.
summary_json_file_name = REPORTS_FOLDER / "invoice_summary.json"

# This opens the JSON file in write mode.
# encoding="utf-8" helps save text correctly.
with open(summary_json_file_name, mode="w", encoding="utf-8") as json_file:
    # This saves the summary data in JSON format.
    # indent=4 makes the JSON easy to read.
    json.dump(summary_data, json_file, indent=4)

# This message tells the user the summary JSON was created.
print(f"Summary JSON created: {summary_json_file_name}")

# This creates a bar chart with invoice status counts.
# A bar chart helps compare categories.
status_counts.plot(kind="bar", color=["orange", "green"])

# This adds a chart title.
plt.title("Invoice Status Counts")

# This adds a label to the x axis.
plt.xlabel("Status")

# This adds a label to the y axis.
plt.ylabel("Number of Invoices")

# This keeps the labels easy to read.
plt.xticks(rotation=0)

# This adjusts the chart layout.
plt.tight_layout()

# This saves the chart inside the reports folder.
plt.savefig(REPORTS_FOLDER / "status_counts.png")

# This clears the chart memory before the next chart.
plt.clf()

# This message tells the user the chart was created.
print("Chart created: status_counts.png")

# This creates a bar chart with risk score by invoice.
# It helps us see invoice risk levels.
plt.bar(df["invoice_number"], df["risk_score"], color="steelblue")

# This adds a chart title.
plt.title("Risk Score by Invoice")

# This adds a label to the x axis.
plt.xlabel("Invoice Number")

# This adds a label to the y axis.
plt.ylabel("Risk Score")

# This adjusts the chart layout.
plt.tight_layout()

# This saves the chart inside the reports folder.
plt.savefig(REPORTS_FOLDER / "risk_scores.png")

# This clears the chart memory.
plt.clf()

# This message tells the user the chart was created.
print("Chart created: risk_scores.png")
