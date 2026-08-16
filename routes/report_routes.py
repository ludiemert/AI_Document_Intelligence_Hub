# This file controls BI report pages.
# It keeps report routes outside app.py.

# This imports Blueprint and render_template from Flask.
# Blueprint helps split Flask routes into files.
from flask import Blueprint, render_template

# This creates the reports blueprint.
# Flask will use it for report pages.
report_bp = Blueprint("report", __name__)


@report_bp.route("/reports")
def reports_page():
    """Show the BI reports page."""
    # This shows the reports.html page.
    return render_template("reports.html")
