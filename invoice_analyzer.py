# This project analyzes business invoices.
# This is the first small step of the AI Document Intelligence Hub.

# This imports csv from Python.
# We use csv to save invoice results in a table file.
import csv

# This imports date from Python.
# We use date to check if the invoice is overdue.
from datetime import date

# This imports Path from Python.
# We use Path to work with folder and file paths.
from pathlib import Path

# This is the reports folder path.
# The app saves output files in this folder.
REPORTS_FOLDER = Path("reports")
# This creates the reports folder if it does not exist.
REPORTS_FOLDER.mkdir(exist_ok=True)

# This is the sample documents folder path.
# The app reads invoice text files from this folder.
SAMPLE_DOCUMENTS_FOLDER = Path("sample_documents")

# This creates the sample documents folder if it does not exist.
SAMPLE_DOCUMENTS_FOLDER.mkdir(exist_ok=True)


# This function finds invoice data in the text.
# A function is a block of code that we can use many times.
def extract_invoice_fields(text):
    """Extract invoice fields from text."""
    # This dictionary will save the invoice fields.
    # A dictionary stores data with key and value.
    fields = {}

    # This line removes extra spaces and splits the text into lines.
    # Now Python can read one line at a time.
    lines = text.strip().split("\n")

    # This loop reads each line from the invoice text.
    # A loop repeats an action.
    for line in lines:

        # This condition checks if the line starts with "Invoice Number:".
        # If it is true, Python saves the invoice number.
        if line.startswith("Invoice Number:"):
            fields["invoice_number"] = line.replace("Invoice Number:", "").strip()

        # This condition checks if the line starts with "Supplier:".
        # If it is true, Python saves the supplier name.
        if line.startswith("Supplier:"):
            fields["supplier_name"] = line.replace("Supplier:", "").strip()

        # This condition checks if the line starts with "Invoice Date:".
        # If it is true, Python saves the invoice date.
        if line.startswith("Invoice Date:"):
            fields["invoice_date"] = line.replace("Invoice Date:", "").strip()

        # This condition checks if the line starts with "Due Date:".
        # If it is true, Python saves the due date.
        if line.startswith("Due Date:"):
            fields["due_date"] = line.replace("Due Date:", "").strip()

        # This condition checks if the line starts with "Total:".
        # If it is true, Python saves amount and currency.
        if line.startswith("Total:"):
            total_text = line.replace("Total:", "").strip()

            # This splits total into two parts.
            # Example: "1250.00 EUR" becomes ["1250.00", "EUR"]
            total_parts = total_text.split()

            # This saves the amount as text.
            fields["total_amount"] = total_parts[0]

            # This saves the currency as text.
            fields["currency"] = total_parts[1]

        # This condition checks if the line starts with "VAT Number:".
        # If it is true, Python saves the VAT number.
        if line.startswith("VAT Number:"):
            fields["vat_number"] = line.replace("VAT Number:", "").strip()

    # This returns the dictionary with all invoice fields.
    # Return sends the result back to the code.
    return fields


# This function checks if the invoice has problems.
# It returns status, risk score, and reasons.
def validate_invoice(fields):
    """Check invoice fields and return status, risk score, and reasons."""
    # This list has all required fields for an invoice.
    required_fields = [
        "invoice_number",
        "supplier_name",
        "invoice_date",
        "due_date",
        "total_amount",
        "currency",
        "vat_number",
    ]

    # This list will save fields that are missing.
    missing_fields = []

    # This list will save the reasons for the result.
    reasons = []

    # Risk score starts at zero.
    # Zero means no risk.
    risk_score = 0

    # This loop checks one required field at a time.
    for field in required_fields:

        # This condition checks if the field is missing or empty.
        if field not in fields or fields[field] == "":
            missing_fields.append(field)

    # If there are missing fields, we add risk points.
    if missing_fields:
        risk_score = risk_score + (len(missing_fields) * 15)
        reasons.append(f"Missing fields: {missing_fields}")

    # This gets the total amount from the fields.
    # Example: "1250.00"
    total_number_text = fields.get("total_amount", "0")

    # This converts text to number.
    # Example: "1250.00" becomes 1250.00
    total_amount = float(total_number_text)

    # If the total is high, we add risk points.
    if total_amount > 5000:
        risk_score = risk_score + 25
        reasons.append("High invoice amount")

    # This gets the due date from the invoice fields.
    # Example: "2026-06-20" becomes a Python date.
    due_date_text = fields.get("due_date", "")

    # This checks if due_date exists.
    if due_date_text:

        # This converts text to a real date.
        # Example: "2026-06-20" becomes a Python date.
        due_date = date.fromisoformat(due_date_text)

        # This checks if the due date is before today.
        # If it is before today, the invoice is overdue.
        if due_date < date.today():
            risk_score = risk_score + 30
            reasons.append("Due date is overdue")

    # If risk_score is zero, the invoice is approved.
    if risk_score == 0:
        status = "approved"
        reasons.append("All required fields are present")

    # If risk_score is lower than 50, the invoice needs review.
    elif risk_score < 50:
        status = "needs_review"

    # If risk_score is 50 or more, the invoice is high risk.
    else:
        status = "high_risk"

    # This returns all validation results.
    return {
        "status": status,
        "risk_score": risk_score,
        "missing_fields": missing_fields,
        "reasons": reasons,
        "total_amount": total_amount,
        "currency": fields.get("currency", ""),
    }


# This function shows the invoice result in the terminal.
# It makes the result easy to read.
def show_result(fields, validation):
    """Show invoice fields and validation result in the terminal."""
    # This title shows the extracted invoice data.
    print("INVOICE FIELDS")
    print("--------------")

    # This loop shows one field per line.
    for field_name, field_value in fields.items():
        print(f"{field_name}: {field_value}")

    # This empty print creates a blank line.
    print()

    # This title shows the validation result.
    print("VALIDATION RESULT")
    print("-----------------")

    # This line shows the invoice status.
    print(f"status: {validation['status']}")

    # This line shows the risk score.
    print(f"risk_score: {validation['risk_score']}")

    # This line shows missing fields.
    print(f"missing_fields: {validation['missing_fields']}")

    # This line shows the reasons.
    print(f"reasons: {validation['reasons']}")


# This function shows a summary of all processed invoices.
# A summary is a short report with important numbers.
def show_summary(results):
    """Show a summary report for all processed invoices."""
    # This counts how many invoices were processed.
    total_invoices = len(results)

    # This variable counts approved invoices.
    approved_count = 0

    # This variable counts invoices that need review.
    needs_review_count = 0

    # This variable counts high risk invoices.
    high_risk_count = 0

    # This variable sums all risk scores.
    total_risk_score = 0

    # This variable sums all invoice amounts.
    total_invoice_amount = 0

    # This variable saves the currency for the summary.
    summary_currency = ""

    # This loop reads one result at a time.
    for result in results:
        # This adds the risk score to the total.
        total_risk_score = total_risk_score + result["risk_score"]
        # This adds the invoice amount to the total amount.
        total_invoice_amount = total_invoice_amount + result["total_amount"]

        # This saves the first currency found.
        # Example: EUR
        if summary_currency == "":
            summary_currency = result["currency"]

        # This checks if the invoice is approved.
        if result["status"] == "approved":
            approved_count = approved_count + 1

        # This checks if the invoice needs review.
        elif result["status"] == "needs_review":
            needs_review_count = needs_review_count + 1

        # This checks if the invoice is high risk.
        elif result["status"] == "high_risk":
            high_risk_count = high_risk_count + 1

    # This calculates the average risk score.
    average_risk_score = total_risk_score / total_invoices

    # This rounds the average risk score to 2 decimal places.
    # Example: 18.333333 becomes 18.33
    average_risk_score = round(average_risk_score, 2)

    # This title shows the summary section.
    print("SUMMARY REPORT")
    print("--------------")

    # These lines show the summary numbers.
    print(f"total_invoices: {total_invoices}")
    print(f"approved: {approved_count}")
    print(f"needs_review: {needs_review_count}")
    print(f"high_risk: {high_risk_count}")
    print(f"average_risk_score: {average_risk_score}")
    # This line shows the total amount with 2 decimal places and currency.
    print(f"total_invoice_amount: {total_invoice_amount:.2f} {summary_currency}")


# This function reads invoice text files from the sample documents folder.
# It returns a list with invoice text and file path.
def load_invoice_texts():
    """Load invoice text files and source file paths."""
    # This list will save all invoice documents.
    invoice_documents = []

    # This loop finds all .txt files in this folder and subfolders.
    # rglob means recursive search.
    for file_path in SAMPLE_DOCUMENTS_FOLDER.rglob("*.txt"):
        # This reads the text from one invoice file.
        invoice_text = file_path.read_text(encoding="utf-8")

        # This saves the invoice text and the file path.
        invoice_documents.append(
            {
                "text": invoice_text,
                "source_file": str(file_path),
            }
        )

    # This returns all invoice documents.
    return invoice_documents


# This function controls the program flow.
# It processes many invoices, one by one.
def main():
    """Run the invoice analysis workflow."""
    # This list saves all validation results.
    # Later, we use this list to create a summary.
    all_results = []

    # This line loads invoice documents from .txt files.
    invoice_documents = load_invoice_texts()

    # This checks if there are no invoice files.
    # If the list is empty, the app stops with a clear message.
    if not invoice_documents:
        print("No invoice files found.")
        print("Please add .txt files to the sample_documents folder.")
        return

    # This loop reads one invoice document at a time.
    for invoice_document in invoice_documents:
        # This gets the invoice text from the document.
        invoice_text = invoice_document["text"]

        # This gets the file path from the document.
        source_file = invoice_document["source_file"]

        # This line extracts fields from one invoice text.
        invoice_fields = extract_invoice_fields(invoice_text)

        # This line validates the extracted fields.
        validation_result = validate_invoice(invoice_fields)

        # This dictionary joins invoice fields and validation result.
        # We use it later to save data in CSV.
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

        # This line saves the processed invoice in the all_results list.
        all_results.append(processed_invoice)

        # This line shows the final result.
        show_result(invoice_fields, validation_result)

        # This line separates one invoice result from the next.
        print()
        print("=" * 50)
        print()

    # This line shows the final summary report.
    show_summary(all_results)

    # This line saves all processed invoices in a CSV file.
    save_results_to_csv(all_results)


# This function saves processed invoices in a CSV file.
# CSV is a table file that Excel and Pandas can read.
def save_results_to_csv(results):
    """Save processed invoice results to a CSV file."""
    # This is the CSV file path inside the reports folder.
    file_name = REPORTS_FOLDER / "invoice_results.csv"

    # These are the CSV column names.
    fieldnames = [
        "source_file",
        "invoice_number",
        "supplier_name",
        "invoice_date",
        "due_date",
        "total_amount",
        "currency",
        "status",
        "risk_score",
        "reasons",
    ]

    # This opens the CSV file in write mode.
    # newline="" helps avoid blank lines in Windows.
    with open(file_name, mode="w", newline="", encoding="utf-8") as csv_file:
        # This creates a CSV writer that uses dictionary keys.
        # delimiter=";" helps Excel open columns correctly in Europe.
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

        # This writes the first row with column names.
        writer.writeheader()

        # This writes all processed invoice rows.
        writer.writerows(results)

    # This message tells the user the CSV was created.
    print(f"CSV file created: {file_name}")


# This condition starts the program.
# It runs main() only when we run this file directly.
if __name__ == "__main__":
    main()
