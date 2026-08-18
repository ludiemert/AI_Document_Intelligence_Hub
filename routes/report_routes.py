# This file controls BI report pages.
# It keeps report routes outside app.py.

# This imports Flask tools.
# We use them for pages, messages, redirects, forms, URLs, and file downloads.
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

# This imports Path from Python.
# We use Path to work with report files.
from pathlib import Path

# This imports the exporter function.
# It creates CSV and JSON reports from SQLite.
from services.exporter import export_invoices_from_sqlite

# This creates the reports blueprint.
# Flask will use it for report pages.
report_bp = Blueprint("report", __name__)


@report_bp.route("/reports")
def reports_page():
    """Show the BI reports page."""
    # This shows the reports.html page.
    return render_template("reports.html")


# This is the reports folder path.
# The app saves and downloads report files from this folder.
REPORTS_FOLDER = Path("reports")


# This route receives the report form.
# It uses POST because the form sends selected filters.
@report_bp.route("/export", methods=["POST"])
def export_reports():
    """Generate filtered BI reports."""
    # This gets the selected year from the form.
    selected_year = request.form.get("year", "all")

    # This gets the selected month from the form.
    selected_month = request.form.get("month", "all")

    # This exports reports using selected filters.
    result = export_invoices_from_sqlite(selected_year, selected_month)

    # This shows a success or error message.
    if result["success"]:
        flash(result["message"], "success")
    else:
        flash(result["message"], "error")

    # This redirects back to the BI reports page.
    return redirect(url_for("report.reports_page"))


@report_bp.route("/download/csv")
def download_invoice_csv():
    """Download the filtered invoice CSV report."""
    # This gets selected filters from the URL.
    selected_year = request.args.get("year", "all")
    selected_month = request.args.get("month", "all")

    # This creates the file name using selected filters.
    file_name = f"invoices_{selected_year}_{selected_month}.csv"

    # This creates the file path.
    file_path = REPORTS_FOLDER / file_name

    # This creates the report if it does not exist yet.
    if not file_path.exists():
        export_invoices_from_sqlite(selected_year, selected_month)

    # This sends the CSV file to the browser.
    return send_file(file_path, as_attachment=True)


@report_bp.route("/download/json")
def download_invoice_json():
    """Download the filtered invoice JSON report."""
    # This gets selected filters from the URL.
    selected_year = request.args.get("year", "all")
    selected_month = request.args.get("month", "all")

    # This creates the file name using selected filters.
    file_name = f"invoices_{selected_year}_{selected_month}.json"

    # This creates the file path.
    file_path = REPORTS_FOLDER / file_name

    # This creates the report if it does not exist yet.
    if not file_path.exists():
        export_invoices_from_sqlite(selected_year, selected_month)

    # This sends the JSON file to the browser.
    return send_file(file_path, as_attachment=True)


@report_bp.route("/download/monthly")
def download_monthly_summary():
    """Download the filtered monthly summary CSV report."""
    # This gets selected filters from the URL.
    selected_year = request.args.get("year", "all")
    selected_month = request.args.get("month", "all")

    # This creates the file name using selected filters.
    file_name = f"monthly_summary_{selected_year}_{selected_month}.csv"

    # This creates the file path.
    file_path = REPORTS_FOLDER / file_name

    # This creates the report if it does not exist yet.
    if not file_path.exists():
        export_invoices_from_sqlite(selected_year, selected_month)

    # This sends the monthly summary file to the browser.
    return send_file(file_path, as_attachment=True)


@report_bp.route("/download/yearly")
def download_yearly_summary():
    """Download the filtered yearly summary CSV report."""
    # This gets selected filters from the URL.
    selected_year = request.args.get("year", "all")
    selected_month = request.args.get("month", "all")

    # This creates the file name using selected filters.
    file_name = f"yearly_summary_{selected_year}_{selected_month}.csv"

    # This creates the file path.
    file_path = REPORTS_FOLDER / file_name

    # This creates the report if it does not exist yet.
    if not file_path.exists():
        export_invoices_from_sqlite(selected_year, selected_month)

    # This sends the yearly summary file to the browser.
    return send_file(file_path, as_attachment=True)


@report_bp.route("/download/risk")
def download_risk_summary():
    """Download the filtered risk summary CSV report."""
    # This gets selected filters from the URL.
    selected_year = request.args.get("year", "all")
    selected_month = request.args.get("month", "all")

    # This creates the file name using selected filters.
    file_name = f"risk_summary_{selected_year}_{selected_month}.csv"

    # This creates the file path.
    file_path = REPORTS_FOLDER / file_name

    # This creates the report if it does not exist yet.
    if not file_path.exists():
        export_invoices_from_sqlite(selected_year, selected_month)

    # This sends the risk summary file to the browser.
    return send_file(file_path, as_attachment=True)
