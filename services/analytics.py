# This file has analytics functions.
# Analytics means reading data and calculating useful numbers.


# This function shows invoice data in the terminal.
# It helps us see the table before calculations.
def show_invoice_data(df):
    """Show invoice data in the terminal."""
    print("INVOICE DATA")
    print("------------")
    print(df)
    print()


# This function counts invoices by status.
# Example: approved, needs_review, high_risk.
def calculate_status_counts(df):
    """Count invoices by status."""
    # This counts invoices by status.
    status_counts = df["status"].value_counts()

    print("STATUS COUNTS")
    print("-------------")
    print(status_counts)
    print()

    # This returns the status count table.
    return status_counts


# This function calculates the main business metrics.
# It returns total amount, average risk, and review percentage.
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

    # This returns the metrics as a dictionary.
    return {
        "total_invoice_amount": float(total_invoice_amount),
        "average_risk_score": float(average_risk_score),
        "needs_review_percentage": float(needs_review_percentage),
    }
