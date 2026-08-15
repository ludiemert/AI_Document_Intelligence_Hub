# This file controls dashboard routes.
# It shows the dashboard, API data, and invoice detail page.

# This imports Flask tools.
# Blueprint helps split routes into smaller files.
from flask import Blueprint, jsonify, render_template

# This imports invoice repository functions.
# They read invoice data from SQLite.
from services.invoice_repository import find_invoice_by_number, load_invoices

# This creates the dashboard blueprint.
# A blueprint is a small group of Flask routes.
dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    """Show the dashboard page."""
    # This sends index.html to the browser.
    return render_template("index.html")


@dashboard_bp.route("/api/invoices")
def get_invoices():
    """Return invoice data as JSON."""
    # This loads invoices from SQLite.
    invoices = load_invoices()

    # This sends invoice data to the frontend.
    return jsonify(invoices)


@dashboard_bp.route("/invoice/<invoice_number>")
def invoice_detail(invoice_number):
    """Show one invoice detail page."""
    # This finds one invoice by invoice number.
    selected_invoice = find_invoice_by_number(invoice_number)

    # This shows an error if the invoice was not found.
    if selected_invoice is None:
        return "Invoice not found", 404

    # This sends one invoice to the detail page.
    return render_template("invoice_detail.html", invoice=selected_invoice)
