# This project analyzes invoice results with Pandas.
# Pandas helps us work with table data.

# This imports pandas.
# We use pandas to read and analyze CSV files.
import pandas as pd

# This is the CSV file created by invoice_analyzer.py.
file_name = "invoice_results.csv"

# This reads the CSV file and creates a DataFrame.
# A DataFrame is a table in Pandas.
df = pd.read_csv(file_name)

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
