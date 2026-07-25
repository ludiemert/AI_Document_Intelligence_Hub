# This file processes one uploaded invoice.
# It extracts data, validates risk, and saves the invoice.

# This imports the extractor function.
# It gets invoice fields from text.
from services.extractor import extract_invoice_fields

# This imports the save function.
# It saves invoice data into SQLite.
from services.invoice_repository import save_invoice

# This imports the validator function.
# It checks invoice fields and creates risk data.
from services.validator import validate_invoice


def process_invoice_text(invoice_text, source_file):
    """Process one invoice text and save it."""
    # This extracts fields from invoice text.
    invoice_fields = extract_invoice_fields(invoice_text)

    # This validates the extracted fields.
    validation_result = validate_invoice(invoice_fields)

    # This creates the final invoice data.
    invoice_data = {
        "source_file": source_file,
        "invoice_number": invoice_fields.get("invoice_number"),
        "supplier_name": invoice_fields.get("supplier_name"),
        "invoice_date": invoice_fields.get("invoice_date"),
        "due_date": invoice_fields.get("due_date"),
        "total_amount": invoice_fields.get("total_amount"),
        "currency": invoice_fields.get("currency"),
        "vat_number": invoice_fields.get("vat_number"),
        "status": validation_result.get("status"),
        "risk_score": validation_result.get("risk_score"),
        "reasons": ", ".join(validation_result.get("reasons", [])),
    }

    # This saves the invoice into SQLite.
    save_invoice(invoice_data)

    # This returns the processed invoice.
    return invoice_data
