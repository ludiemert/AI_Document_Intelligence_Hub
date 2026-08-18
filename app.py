# This imports Flask.
# Flask starts the web application.
from flask import Flask

# This imports dashboard routes.
# Dashboard routes control the dashboard, API, and invoice detail page.
from routes.dashboard_routes import dashboard_bp

# This imports report routes.
# Report routes control BI reports, export, and downloads.
from routes.report_routes import report_bp

# This imports upload routes.
# Upload routes control TXT upload and OCR upload.
from routes.upload_routes import upload_bp

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

# This registers dashboard routes.
# Flask now knows the dashboard blueprint.
app.register_blueprint(dashboard_bp)

# This registers upload routes.
# Flask now knows the upload blueprint.
app.register_blueprint(upload_bp)

# This registers report routes.
# Flask now knows the BI reports blueprint.
app.register_blueprint(report_bp)


# This starts the Flask app.
# debug=True helps us see errors while learning.
if __name__ == "__main__":
    app.run(debug=True)
