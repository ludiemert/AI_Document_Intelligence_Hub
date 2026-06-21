# This file creates summary tables.
# Summary tables help business reports and dashboards.


# This function creates a monthly summary report.
# It groups invoices by year and month.
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

    # This returns the monthly summary table.
    return monthly_summary


# This function creates a monthly status summary report.
# It groups invoices by year, month, and status.
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

    # This returns the monthly status summary table.
    return monthly_status_summary
