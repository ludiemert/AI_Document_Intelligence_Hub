# This project analyzes invoice results with Pandas.
# Pandas helps us work with table data.

# This imports pandas.
# We use pandas to read and analyze CSV files.
import pandas as pd

# This is the CSV file created by invoice_analyzer.py.
file_name = "invoice_results.csv"

# This reads the CSV file and creates a DataFrame.
# sep=";" means the CSV uses semicolon as separator.
df = pd.read_csv(file_name, sep=";")

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

# This dictionary saves the business metrics.
# We use it to create a summary CSV file.
summary_data = {
    "total_invoices": len(df),
    "approved": status_counts.get("approved", 0),
    "needs_review": status_counts.get("needs_review", 0),
    "high_risk": status_counts.get("high_risk", 0),
    "average_risk_score": average_risk_score,
    "total_invoice_amount": total_invoice_amount,
    "currency": "EUR",
}

# This converts the summary dictionary into a DataFrame.
# Pandas needs a list to create one row.
summary_df = pd.DataFrame([summary_data])

# This is the summary CSV file name.
summary_file_name = "invoice_summary.csv"

# This saves the summary DataFrame as a CSV file.
# sep=";" helps Excel open columns correctly in Europe.
# index=False avoids an extra number column.
summary_df.to_csv(summary_file_name, sep=";", index=False)

# This message tells the user the summary CSV was created.
print(f"Summary CSV created: {summary_file_name}")
