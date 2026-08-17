# This file controls BI report pages.
# It keeps report routes outside app.py.

# This imports Flask tools.
# We use them for pages, messages, redirects, and form data.
from flask import Blueprint, flash, redirect, render_template, request, url_for

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
