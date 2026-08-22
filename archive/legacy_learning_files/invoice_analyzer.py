# This file controls the invoice analysis workflow.
# It uses service files to do each job.

# This imports the function that saves results in CSV.
from services.csv_exporter import save_results_to_csv

# This imports the function that loads invoice text files.
from services.document_loader import load_invoice_texts

# This imports the function that extracts invoice fields.
from services.extractor import extract_invoice_fields

# This imports the functions that show results in the terminal.
from services.reporter import show_result, show_summary

# This imports the function that validates invoice data.
from services.validator import validate_invoice


# This function controls the full invoice workflow.
# It loads documents, extracts data, validates data, and saves results.
def main():
    """Run the invoice analysis workflow."""
    # This list saves all processed invoice results.
    all_results = []

    # This line loads invoice documents from .txt files.
    invoice_documents = load_invoice_texts()

    # This checks if there are no invoice files.
    # If there are no files, the app stops safely.
    if not invoice_documents:
        print("No invoice files found.")
        print("Please add .txt files to the sample_documents folder.")
        return

    # This loop reads one invoice document at a time.
    for invoice_document in invoice_documents:
        # This gets the invoice text from the document.
        invoice_text = invoice_document["text"]

        # This gets the source file path.
        source_file = invoice_document["source_file"]

        # This extracts fields from the invoice text.
        invoice_fields = extract_invoice_fields(invoice_text)

        # This validates the extracted invoice fields.
        validation_result = validate_invoice(invoice_fields)

        # This dictionary joins invoice fields and validation result.
        # It creates one clean row for the CSV file.
        processed_invoice = {
            "source_file": source_file,
            "invoice_number": invoice_fields.get("invoice_number", ""),
            "supplier_name": invoice_fields.get("supplier_name", ""),
            "invoice_date": invoice_fields.get("invoice_date", ""),
            "due_date": invoice_fields.get("due_date", ""),
            "total_amount": validation_result["total_amount"],
            "currency": validation_result["currency"],
            "status": validation_result["status"],
            "risk_score": validation_result["risk_score"],
            "reasons": "; ".join(validation_result["reasons"]),
        }

        # This saves the processed invoice in the results list.
        all_results.append(processed_invoice)

        # This shows the invoice result in the terminal.
        show_result(invoice_fields, validation_result)

        # This separates one invoice result from the next.
        print()
        print("=" * 50)
        print()

    # This shows the final summary report.
    show_summary(all_results)

    # This saves all processed invoices in a CSV file.
    save_results_to_csv(all_results)


# This condition starts the program.
# It runs main() only when we run this file directly.
if __name__ == "__main__":
    main()
