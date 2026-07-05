# This imports Flask tools.
# Flask creates the web backend and API.
from flask import Flask, jsonify, render_template

# This imports json from Python.
# We use json to read invoice data.
import json

# This imports Path from Python.
# Path helps us work with files and folders.
from pathlib import Path

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


@app.route("/")
def dashboard():
    """Show the dashboard page."""
    # This sends index.html to the browser.
    return render_template("index.html")


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
