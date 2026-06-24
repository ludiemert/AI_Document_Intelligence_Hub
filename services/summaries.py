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


# This function creates a yearly summary report.
# It groups invoices by year and calculates business metrics.
def create_yearly_summary(df):
    """Create a yearly summary report."""
    # This groups invoices by year.
    yearly_summary = (
        df.groupby("invoice_year")
        .agg(
            total_invoices=("invoice_number", "count"),
            total_invoice_amount=("total_amount", "sum"),
            average_risk_score=("risk_score", "mean"),
        )
        .reset_index()
    )

    # This rounds the average risk score to 2 decimal places.
    yearly_summary["average_risk_score"] = yearly_summary["average_risk_score"].round(2)

    # This counts statuses by year.
    yearly_status_counts = (
        df.groupby(["invoice_year", "status"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # This joins yearly metrics with yearly status counts.
    yearly_summary = yearly_summary.merge(
        yearly_status_counts,
        on="invoice_year",
        how="left",
    )

    # These columns must exist even if the count is zero.
    for status in ["approved", "needs_review", "high_risk"]:
        if status not in yearly_summary.columns:
            yearly_summary[status] = 0

    print()
    print("YEARLY SUMMARY")
    print("--------------")
    print(yearly_summary)

    # This returns the yearly summary table.
    return yearly_summary
