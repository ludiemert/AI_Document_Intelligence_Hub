# This imports Flask tools.
# Flask creates the app, messages, redirects, pages, requests, and downloads.
from flask import Flask, flash, redirect, render_template, request, send_file, url_for

# This imports Path from Python.
# Path helps us work with folders and files.
from pathlib import Path

# This imports report routes.
# Report routes control BI report pages.
from routes.report_routes import report_bp

# This imports dashboard routes.
# These routes control dashboard, API, and invoice detail.
from routes.dashboard_routes import dashboard_bp

# This imports upload routes.
# These routes control TXT upload, image OCR upload, and PDF pending OCR.
from routes.upload_routes import upload_bp

# This imports the export function.
# We use it to create CSV and JSON reports from SQLite.
from services.exporter import export_invoices_from_sqlite

# This creates the Flask app.
# template_folder tells Flask where the HTML files are.
# static_folder tells Flask where CSS and JS files are.
app = Flask(
    __name__,
    template_folder="frontend",
    static_folder="frontend",
)

# This registers dashboard routes.
# Flask now knows the dashboard blueprint.
app.register_blueprint(dashboard_bp)

# This registers upload routes.
# Flask now knows the upload blueprint.
app.register_blueprint(upload_bp)

# This registers report routes.
# Flask now knows the BI reports blueprint.
app.register_blueprint(report_bp)

# This secret key lets Flask show temporary messages.
# We use this for success and error messages.
app.secret_key = "dev-secret-key"

# This is the reports folder path.
# Flask saves and downloads reports from this folder.
REPORTS_FOLDER = Path("reports")

# This is the uploads folder path.
# Flask saves uploaded invoice files in this folder.
UPLOADS_FOLDER = Path("uploads")

# This is the pending OCR folder path.
# PDF and image files wait here for OCR processing.
PENDING_OCR_FOLDER = UPLOADS_FOLDER / "pending_ocr"

# This set has the file types accepted by the app.
# TXT works now. PDF and images will be prepared for OCR later.
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg"}

# This creates the reports folder if it does not exist.
REPORTS_FOLDER.mkdir(exist_ok=True)

# This creates the uploads folder if it does not exist.
UPLOADS_FOLDER.mkdir(exist_ok=True)

# This creates the pending OCR folder if it does not exist.
PENDING_OCR_FOLDER.mkdir(parents=True, exist_ok=True)


def allowed_file(filename):
    """Check if the uploaded file type is allowed."""
    # This checks if the file name has a dot.
    if "." not in filename:
        return False

    # This gets the file extension after the last dot.
    file_extension = filename.rsplit(".", 1)[1].lower()

    # This checks if the extension is in the allowed list.
    return file_extension in ALLOWED_EXTENSIONS


def get_file_extension(filename):
    """Get the uploaded file extension."""
    # This gets the file extension after the last dot.
    file_extension = filename.rsplit(".", 1)[1].lower()

    # This returns the file extension.
    return file_extension


@app.route("/export")
def export_reports():
    """Export invoice reports from SQLite using selected filters."""
    # This gets the selected year from the BI Reports page.
    selected_year = request.args.get("year", "all")

    # This gets the selected month from the BI Reports page.
    selected_month = request.args.get("month", "all")

    # This exports invoices using the selected filters.
    export_result = export_invoices_from_sqlite(selected_year, selected_month)

    # This checks if the export failed.
    if not export_result["success"]:
        flash(export_result["message"], "error")
        return redirect(url_for("reports_page"))

    # This shows a success message to the user.
    flash(
        f"Reports exported: {export_result['csv_file']} and {export_result['json_file']}",
        "success",
    )

    # This sends the user back to the BI Reports page.
    return redirect(url_for("reports_page"))


@app.route("/download/csv")
def download_csv_report():
    """Download a CSV report."""
    # This gets selected year from the URL.
    selected_year = request.args.get("year", "all")

    # This gets selected month from the URL.
    selected_month = request.args.get("month", "all")

    # This creates the report file name.
    report_name = f"invoices_{selected_year}_{selected_month}"

    # This is the CSV file path.
    csv_file_path = REPORTS_FOLDER / f"{report_name}.csv"

    # This creates the report if it does not exist yet.
    if not csv_file_path.exists():
        export_invoices_from_sqlite(selected_year, selected_month)

    # This sends the CSV file to the browser.
    return send_file(csv_file_path, as_attachment=True)


@app.route("/download/json")
def download_json_report():
    """Download a JSON report."""
    # This gets selected year from the URL.
    selected_year = request.args.get("year", "all")

    # This gets selected month from the URL.
    selected_month = request.args.get("month", "all")

    # This creates the report file name.
    report_name = f"invoices_{selected_year}_{selected_month}"

    # This is the JSON file path.
    json_file_path = REPORTS_FOLDER / f"{report_name}.json"

    # This creates the report if it does not exist yet.
    if not json_file_path.exists():
        export_invoices_from_sqlite(selected_year, selected_month)

    # This sends the JSON file to the browser.
    return send_file(json_file_path, as_attachment=True)


@app.route("/download/monthly")
def download_monthly_summary():
    """Download the monthly summary report."""
    # This gets selected year from the URL.
    selected_year = request.args.get("year", "all")

    # This gets selected month from the URL.
    selected_month = request.args.get("month", "all")

    # This creates the monthly summary file name.
    file_name = f"monthly_summary_{selected_year}_{selected_month}.csv"

    # This creates the monthly summary file path.
    file_path = REPORTS_FOLDER / file_name

    # This creates the report if it does not exist yet.
    if not file_path.exists():
        export_invoices_from_sqlite(selected_year, selected_month)

    # This sends the monthly summary file to the browser.
    return send_file(file_path, as_attachment=True)


@app.route("/download/yearly")
def download_yearly_summary():
    """Download the yearly summary report."""
    # This gets selected year from the URL.
    selected_year = request.args.get("year", "all")

    # This gets selected month from the URL.
    selected_month = request.args.get("month", "all")

    # This creates the yearly summary file name.
    file_name = f"yearly_summary_{selected_year}_{selected_month}.csv"

    # This creates the yearly summary file path.
    file_path = REPORTS_FOLDER / file_name

    # This creates the report if it does not exist yet.
    if not file_path.exists():
        export_invoices_from_sqlite(selected_year, selected_month)

    # This sends the yearly summary file to the browser.
    return send_file(file_path, as_attachment=True)


@app.route("/download/risk")
def download_risk_summary():
    """Download the risk summary report."""
    # This gets selected year from the URL.
    selected_year = request.args.get("year", "all")

    # This gets selected month from the URL.
    selected_month = request.args.get("month", "all")

    # This creates the risk summary file name.
    file_name = f"risk_summary_{selected_year}_{selected_month}.csv"

    # This creates the risk summary file path.
    file_path = REPORTS_FOLDER / file_name

    # This creates the report if it does not exist yet.
    if not file_path.exists():
        export_invoices_from_sqlite(selected_year, selected_month)

    # This sends the risk summary file to the browser.
    return send_file(file_path, as_attachment=True)


# This starts the Flask app.
# debug=True helps us see errors while learning.
if __name__ == "__main__":
    app.run(debug=True)
