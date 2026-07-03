# This imports Flask tools.
# Flask creates the web backend and API.
from flask import Flask, jsonify, render_template

# This imports json from Python.
# We use json to read invoice data.
import json

# This imports Path from Python.
# Path helps us work with files and folders.
from pathlib import Path

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
    # This is the invoice JSON file path.
    file_path = REPORTS_FOLDER / "invoice_results.json"

    # This opens the JSON file created by Python.
    with open(file_path, mode="r", encoding="utf-8") as json_file:
        invoices = json.load(json_file)

    # This sends invoice data to the frontend.
    return jsonify(invoices)


@app.route("/invoice/<invoice_number>")
def invoice_detail(invoice_number):
    """Show one invoice detail page."""
    # This is the invoice JSON file path.
    file_path = REPORTS_FOLDER / "invoice_results.json"

    # This opens the JSON file created by Python.
    with open(file_path, mode="r", encoding="utf-8") as json_file:
        invoices = json.load(json_file)

    # This finds one invoice by invoice number.
    selected_invoice = None

    # This checks each invoice.
    for invoice in invoices:
        if invoice["invoice_number"] == invoice_number:
            selected_invoice = invoice
            break

    # This shows an error if the invoice was not found.
    if selected_invoice is None:
        return "Invoice not found", 404

    # This sends one invoice to the detail page.
    return render_template("invoice_detail.html", invoice=selected_invoice)


# This starts the Flask app.
# debug=True helps us see errors while learning.
if __name__ == "__main__":
    app.run(debug=True)
