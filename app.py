# This imports Flask tools.
# Flask creates the web backend and API.
# Flask creates pages, APIs, redirects, and receives files.
from flask import Flask, jsonify, redirect, render_template, request, url_for

# This imports json from Python.
# We use json to read invoice data.
import json

# This imports Path from Python.
# Path helps us work with files and folders.
from pathlib import Path

# This imports invoice data functions.
# The repository reads invoice data for Flask.
from services.invoice_repository import find_invoice_by_number, load_invoices

# This imports the invoice processor.
# It processes uploaded invoice text.
from services.invoice_processor import process_invoice_text

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

        # This creates the file path inside uploads folder.
        file_path = UPLOADS_FOLDER / uploaded_file.filename

        # This saves the uploaded file.
        uploaded_file.save(file_path)

        # This reads the uploaded text file.
        invoice_text = file_path.read_text(encoding="utf-8")

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
