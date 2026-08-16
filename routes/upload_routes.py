# This file controls upload routes.
# It receives TXT, PDF, and image invoice files.

# This imports Flask tools.
# Blueprint helps split upload routes into this file.
from flask import Blueprint, flash, redirect, render_template, request, url_for

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
# It reads invoice fields from text.
from services.extractor import extract_invoice_fields

# This imports the invoice processor.
# It saves processed invoice data into SQLite.
from services.invoice_processor import process_invoice_text

# This imports the OCR reader function.
# It reads TXT files and image files.
from services.ocr_reader import read_text_from_file

# This creates the upload blueprint.
# A blueprint is a small group of Flask routes.
upload_bp = Blueprint("upload", __name__)

# This is the uploads folder path.
# Flask saves uploaded invoice files in this folder.
UPLOADS_FOLDER = Path("uploads")

# This is the pending OCR folder path.
# PDF and image files wait here for OCR processing.
PENDING_OCR_FOLDER = UPLOADS_FOLDER / "pending_ocr"

# This set has the file types accepted by the app.
# TXT and image OCR work now. PDF is saved for future OCR.
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg"}

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


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload_invoice_page():
    """Show upload page and process uploaded invoice."""
    # This checks if the user submitted the form.
    if request.method == "POST":
        # This gets the uploaded file from the form.
        uploaded_file = request.files.get("invoice_file")

        # This checks if no file was uploaded.
        if uploaded_file is None or uploaded_file.filename == "":
            flash("No file uploaded. Please choose an invoice file.", "error")
            return redirect(url_for("upload.upload_invoice_page"))

        # This checks if the uploaded file type is allowed.
        if not allowed_file(uploaded_file.filename):
            flash(
                "Invalid file type. Please upload TXT, PDF, PNG, JPG, or JPEG.",
                "error",
            )
            return redirect(url_for("upload.upload_invoice_page"))

        # This gets the uploaded file extension.
        file_extension = get_file_extension(uploaded_file.filename)

        # This checks if the file is PDF.
        # PDF OCR will be added later.
        if file_extension == "pdf":
            pending_file_path = PENDING_OCR_FOLDER / uploaded_file.filename
            uploaded_file.save(pending_file_path)

            flash("PDF uploaded successfully. PDF OCR will be added next.", "success")
            return redirect(url_for("upload.upload_invoice_page"))

        # This checks if the file is an image.
        # Image files can be processed with OCR now.
        elif file_extension in ["png", "jpg", "jpeg"]:
            pending_file_path = PENDING_OCR_FOLDER / uploaded_file.filename
            uploaded_file.save(pending_file_path)

            text_result = read_text_from_file(pending_file_path)

            if not text_result["success"]:
                flash(text_result["message"], "error")
                return redirect(url_for("upload.upload_invoice_page"))

            invoice_text = text_result["text"]

        # This checks if the file is TXT.
        # TXT files are read as normal text.
        elif file_extension == "txt":
            temp_file_path = UPLOADS_FOLDER / uploaded_file.filename
            uploaded_file.save(temp_file_path)

            text_result = read_text_from_file(temp_file_path)

            if not text_result["success"]:
                flash(text_result["message"], "error")
                return redirect(url_for("upload.upload_invoice_page"))

            invoice_text = text_result["text"]

        # This stops the upload if the file type is not expected.
        # This is a safety check.
        else:
            flash("Invalid file type.", "error")
            return redirect(url_for("upload.upload_invoice_page"))

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
            return redirect(url_for("upload.upload_invoice_page"))

        # This gets invoice number from extracted fields.
        invoice_number = invoice_fields.get("invoice_number")

        # This checks if invoice number has the correct format.
        if not re.fullmatch(r"INV-\d{4}-\d{3,}", invoice_number):
            flash("Invalid invoice number. Example: INV-2027-001", "error")
            return redirect(url_for("upload.upload_invoice_page"))

        # This gets invoice date from extracted fields.
        invoice_date = invoice_fields.get("invoice_date")

        # This checks if invoice date has the correct format.
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", invoice_date):
            flash("Invalid invoice date. Please use format YYYY-MM-DD.", "error")
            return redirect(url_for("upload.upload_invoice_page"))

        # This checks if invoice date is a real calendar date.
        try:
            datetime.strptime(invoice_date, "%Y-%m-%d")
        except ValueError:
            flash("Invalid invoice date. Please use a real date.", "error")
            return redirect(url_for("upload.upload_invoice_page"))

        # This gets due date from extracted fields.
        due_date = invoice_fields.get("due_date")

        # This checks if due date has the correct format.
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", due_date):
            flash("Invalid due date. Please use format YYYY-MM-DD.", "error")
            return redirect(url_for("upload.upload_invoice_page"))

        # This checks if due date is a real calendar date.
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            flash("Invalid due date. Please use a real date.", "error")
            return redirect(url_for("upload.upload_invoice_page"))

        # This gets the total amount.
        total_amount = invoice_fields.get("total_amount")

        # This checks if total amount is a valid number.
        try:
            float(total_amount)
        except ValueError:
            flash("Invalid total amount. Please use a number like 1250.00.", "error")
            return redirect(url_for("upload.upload_invoice_page"))

        # This gets currency from extracted fields.
        currency = invoice_fields.get("currency")

        # This checks if currency is EUR.
        if currency != "EUR":
            flash("Invalid currency. This app currently accepts only EUR.", "error")
            return redirect(url_for("upload.upload_invoice_page"))

        # This gets year and month from invoice date.
        invoice_year = invoice_date[:4]
        invoice_month = invoice_date[5:7]

        # This creates the upload folder by year and month.
        target_folder = UPLOADS_FOLDER / invoice_year / invoice_month
        target_folder.mkdir(parents=True, exist_ok=True)

        # This checks if the uploaded file is TXT.
        if file_extension == "txt":
            file_path = target_folder / uploaded_file.filename
            file_path.write_text(invoice_text, encoding="utf-8")

        # This saves OCR text from image files.
        else:
            extracted_text_file_name = f"{Path(uploaded_file.filename).stem}_ocr.txt"
            file_path = target_folder / extracted_text_file_name
            file_path.write_text(invoice_text, encoding="utf-8")

        # This sets the source type for SQLite.
        # TXT upload is txt. Image OCR upload is ocr_image.
        if file_extension == "txt":
            source_type = "txt"
        else:
            source_type = "ocr_image"

        # This processes the invoice and saves it into SQLite.
        process_invoice_text(invoice_text, str(file_path), source_type)

        # This shows a success message after processing.
        flash(f"Invoice processed successfully: {invoice_number}", "success")

        # This redirects the user back to the dashboard.
        return redirect(url_for("dashboard.dashboard"))

    # This shows the upload page.
    return render_template("upload.html")
