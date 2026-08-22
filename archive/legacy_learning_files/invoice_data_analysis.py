# This file controls the invoice data analysis workflow.
# It uses service files to analyze data and create reports.

# This imports Path from Python.
# We use Path to work with folder and file paths.
from pathlib import Path

# This imports data loading functions.
from services.analysis_loader import add_date_columns, load_invoice_data

# This imports analytics functions.
from services.analytics import (
    calculate_business_metrics,
    calculate_status_counts,
    show_invoice_data,
)

# This imports chart builder functions.
from services.chart_builder import (
    create_monthly_status_chart,
    create_risk_score_chart,
    create_status_chart,
    create_yearly_amount_chart,
    create_yearly_risk_chart,
)

# This imports recommendation functions.
from services.recommendations import create_recommendation, create_yearly_recommendation

# This imports report exporter functions.
from services.report_exporter import (
    save_business_recommendations,
    save_monthly_reports,
    save_summary_files,
    save_yearly_invoice_results,
)

# This imports summary functions.
from services.summaries import (
    create_monthly_status_summary,
    create_monthly_summary,
    create_yearly_summary,
)

# This is the reports folder path.
# The app reads and saves report files in this folder.
REPORTS_FOLDER = Path("reports")

# This creates the reports folder if it does not exist.
REPORTS_FOLDER.mkdir(exist_ok=True)


# This function controls the full data analysis workflow.
# It calls service functions in the correct order.
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

    # This creates yearly summary.
    yearly_summary = create_yearly_summary(df)

    # This creates yearly business recommendation.
    yearly_recommendation = create_yearly_recommendation(yearly_summary)

    # This saves monthly reports.
    save_monthly_reports(REPORTS_FOLDER, monthly_summary, monthly_status_summary)

    # This saves invoice results separated by year.
    save_yearly_invoice_results(REPORTS_FOLDER, df)

    # This saves summary CSV and JSON files.
    save_summary_files(
        REPORTS_FOLDER,
        df,
        status_counts,
        metrics,
        recommendation,
        yearly_recommendation,
    )

    # This saves business recommendations as a separate JSON file.
    save_business_recommendations(
        REPORTS_FOLDER,
        recommendation,
        yearly_recommendation,
    )

    # This creates chart image files.
    create_status_chart(REPORTS_FOLDER, status_counts)
    create_risk_score_chart(REPORTS_FOLDER, df)
    create_monthly_status_chart(REPORTS_FOLDER, monthly_status_summary)

    # This creates yearly amount chart.
    create_yearly_amount_chart(REPORTS_FOLDER, yearly_summary)

    # This creates yearly risk chart.
    create_yearly_risk_chart(REPORTS_FOLDER, yearly_summary)


# This condition starts the program.
# It runs main() only when we run this file directly.
if __name__ == "__main__":
    main()
