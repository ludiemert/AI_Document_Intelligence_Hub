# This imports Flask tools.
# Flask creates pages, APIs, redirects, and receives files.
from flask import Flask, jsonify, redirect, render_template, request, url_for

# This imports Path from Python.
# Path helps us work with folders and files.
from pathlib import Path

# This imports the extractor function.
# We use it to get invoice date before saving the file.
from services.extractor import extract_invoice_fields

# This imports the invoice processor.
# It processes uploaded invoice text.
from services.invoice_processor import process_invoice_text

# This imports invoice data functions.
# The repository reads invoice data for Flask.
from services.invoice_repository import find_invoice_by_number, load_invoices

# This creates the Flask app.
# template_folder tells Flask where the HTML files are.
# static_folder tells Flask where CSS and JS files are.
app = Flask(
    __name__,
    template_folder="frontend",
    static_folder="frontend",
)

# This is the reports folder path.
# Flask will read JSON files from this folder.
REPORTS_FOLDER = Path("reports")

# This is the uploads folder path.
# Flask saves uploaded files in this folder.
UPLOADS_FOLDER = Path("uploads")

# This creates the uploads folder if it does not exist.
UPLOADS_FOLDER.mkdir(exist_ok=True)


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
            return "No file uploaded", 400

        # This reads the uploaded file text.
        invoice_text = uploaded_file.read().decode("utf-8")

        # This extracts fields before saving the file.
        invoice_fields = extract_invoice_fields(invoice_text)

        # This gets invoice date from extracted fields.
        invoice_date = invoice_fields.get("invoice_date")

        # This checks if invoice date was not found.
        # The app needs the date to create year and month folders.
        if not invoice_date:
            return "Invoice date not found in the uploaded file", 400

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

        # This redirects the user back to the dashboard.
        return redirect(url_for("dashboard"))

    # This shows the upload page.
    return render_template("upload.html")


@app.route("/api/invoices")
def get_invoices():
    """Return invoice data as JSON."""
    # This loads invoices from the repository.
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


# This starts the Flask app.
# debug=True helps us see errors while learning.
if __name__ == "__main__":
    app.run(debug=True)
