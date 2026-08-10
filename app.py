# This imports Flask tools.
# Flask creates pages, APIs, redirects, messages, and file downloads.
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

# This imports re from Python.
# We use it to check text patterns.
import re

# This imports datetime from Python.
# We use it to validate real dates.
from datetime import datetime

# This imports Path from Python.
# Path helps us work with folders and files.
from pathlib import Path

# This imports the extractor function.
# We use it to read invoice fields from text.
from services.extractor import extract_invoice_fields

# This imports the export function.
# We use it to create CSV and JSON reports from SQLite.
from services.exporter import export_invoices_from_sqlite

# This imports the invoice processor.
# It processes uploaded invoice text.
from services.invoice_processor import process_invoice_text

# This imports the OCR reader function.
# It reads text from TXT files and prepares OCR files.
from services.ocr_reader import read_text_from_file

# This imports invoice data functions.
# The repository reads invoice data from SQLite.
from services.invoice_repository import find_invoice_by_number, load_invoices

# This creates the Flask app.
# template_folder tells Flask where the HTML files are.
# static_folder tells Flask where CSS and JS files are.
app = Flask(
    __name__,
    template_folder="frontend",
    static_folder="frontend",
)

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


@app.route("/")
def dashboard():
    """Show the dashboard page."""
    # This sends index.html to the browser.
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_invoice_page():
    """Show upload page and process uploaded invoice."""
    # This checks if the user submitted the form.
    if request.method == "POST":
        # This gets the uploaded file from the form.
        uploaded_file = request.files.get("invoice_file")

        # This checks if no file was uploaded.
        if uploaded_file is None or uploaded_file.filename == "":
            flash("No file uploaded. Please choose an invoice file.", "error")
            return redirect(url_for("upload_invoice_page"))

        # This checks if the uploaded file type is allowed.
        # The app accepts txt now. PDF and images will use OCR later.
        if not allowed_file(uploaded_file.filename):
            flash(
                "Invalid file type. Please upload TXT, PDF, PNG, JPG, or JPEG.",
                "error",
            )
            return redirect(url_for("upload_invoice_page"))

        # This gets the uploaded file extension.
        file_extension = get_file_extension(uploaded_file.filename)

        # This checks if the file is PDF.
        # PDF OCR will be added later.
        if file_extension == "pdf":
            # This creates the pending OCR file path.
            pending_file_path = PENDING_OCR_FOLDER / uploaded_file.filename

            # This saves the PDF file for future OCR.
            uploaded_file.save(pending_file_path)

            # This shows a message to the user.
            flash(
                "PDF uploaded successfully. PDF OCR will be added next.",
                "success",
            )

            # This sends the user back to the upload page.
            return redirect(url_for("upload_invoice_page"))

        # This checks if the file is an image.
        # Image files can be processed with OCR now.
        if file_extension in ["png", "jpg", "jpeg"]:
            # This creates the pending OCR file path.
            pending_file_path = PENDING_OCR_FOLDER / uploaded_file.filename

            # This saves the image file for OCR.
            uploaded_file.save(pending_file_path)

            # This reads text from the image using OCR reader.
            text_result = read_text_from_file(pending_file_path)

            # This checks if OCR failed.
            if not text_result["success"]:
                flash(text_result["message"], "error")
                return redirect(url_for("upload_invoice_page"))

            # This gets OCR text from the reader result.
            invoice_text = text_result["text"]

            # This saves the TXT file temporarily.
        # The OCR reader will read text from this saved file.
        temp_file_path = UPLOADS_FOLDER / uploaded_file.filename
        uploaded_file.save(temp_file_path)

        # This reads text using the OCR reader service.
        text_result = read_text_from_file(temp_file_path)

        # This checks if the text reader failed.
        if not text_result["success"]:
            flash(text_result["message"], "error")
            return redirect(url_for("upload_invoice_page"))

        # This gets the invoice text from the reader result.
        invoice_text = text_result["text"]

        # This extracts invoice fields before saving the file.
        invoice_fields = extract_invoice_fields(invoice_text)

        # This list has all required invoice fields.
        required_upload_fields = [
            "invoice_number",
            "supplier_name",
            "invoice_date",
            "due_date",
            "total_amount",
            "currency",
            "vat_number",
        ]

        # This finds required fields that are missing.
        missing_upload_fields = [
            field for field in required_upload_fields if not invoice_fields.get(field)
        ]

        # This stops the upload if required fields are missing.
        if missing_upload_fields:
            flash(
                f"Invalid invoice layout. Missing fields: {', '.join(missing_upload_fields)}",
                "error",
            )
            return redirect(url_for("upload_invoice_page"))

        # This gets invoice number from extracted fields.
        invoice_number = invoice_fields.get("invoice_number")

        # This checks if invoice number has the correct format.
        if not re.fullmatch(r"INV-\d{4}-\d{3,}", invoice_number):
            flash("Invalid invoice number. Example: INV-2027-001", "error")
            return redirect(url_for("upload_invoice_page"))

        # This gets invoice date from extracted fields.
        invoice_date = invoice_fields.get("invoice_date")

        # This checks if invoice date has the correct format.
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", invoice_date):
            flash("Invalid invoice date. Please use format YYYY-MM-DD.", "error")
            return redirect(url_for("upload_invoice_page"))

        # This checks if invoice date is a real calendar date.
        try:
            datetime.strptime(invoice_date, "%Y-%m-%d")
        except ValueError:
            flash("Invalid invoice date. Please use a real date.", "error")
            return redirect(url_for("upload_invoice_page"))

        # This gets due date from extracted fields.
        due_date = invoice_fields.get("due_date")

        # This checks if due date has the correct format.
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", due_date):
            flash("Invalid due date. Please use format YYYY-MM-DD.", "error")
            return redirect(url_for("upload_invoice_page"))

        # This checks if due date is a real calendar date.
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            flash("Invalid due date. Please use a real date.", "error")
            return redirect(url_for("upload_invoice_page"))

        # This gets the total amount.
        total_amount = invoice_fields.get("total_amount")

        # This checks if total amount is a valid number.
        try:
            float(total_amount)
        except ValueError:
            flash("Invalid total amount. Please use a number like 1250.00.", "error")
            return redirect(url_for("upload_invoice_page"))

        # This gets currency from extracted fields.
        currency = invoice_fields.get("currency")

        # This checks if currency is EUR.
        if currency != "EUR":
            flash("Invalid currency. This app currently accepts only EUR.", "error")
            return redirect(url_for("upload_invoice_page"))

        # This gets year and month from invoice date.
        invoice_year = invoice_date[:4]
        invoice_month = invoice_date[5:7]

        # This creates the upload folder by year and month.
        target_folder = UPLOADS_FOLDER / invoice_year / invoice_month

        # This creates the folder if it does not exist.
        target_folder.mkdir(parents=True, exist_ok=True)

        # This creates the final file path.
        file_path = target_folder / uploaded_file.filename

        # This saves the uploaded text into the final file.
        file_path.write_text(invoice_text, encoding="utf-8")

        # This processes the invoice and saves it into SQLite.
        process_invoice_text(invoice_text, str(file_path))

        # This shows a success message after processing.
        flash(f"Invoice processed successfully: {invoice_number}", "success")

        # This redirects the user back to the dashboard.
        return redirect(url_for("dashboard"))

    # This shows the upload page.
    return render_template("upload.html")


@app.route("/api/invoices")
def get_invoices():
    """Return invoice data as JSON."""
    # This loads invoices from SQLite.
    invoices = load_invoices()

    # This sends invoice data to the frontend.
    return jsonify(invoices)


@app.route("/invoice/<invoice_number>")
def invoice_detail(invoice_number):
    """Show one invoice detail page."""
    # This finds one invoice by invoice number.
    selected_invoice = find_invoice_by_number(invoice_number)

    # This shows an error if the invoice was not found.
    if selected_invoice is None:
        return "Invoice not found", 404

    # This sends one invoice to the detail page.
    return render_template("invoice_detail.html", invoice=selected_invoice)


@app.route("/reports")
def reports_page():
    """Show the BI Reports page."""
    # This sends reports.html to the browser.
    return render_template("reports.html")


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
