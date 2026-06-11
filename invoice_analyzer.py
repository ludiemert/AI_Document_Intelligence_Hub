# This project analyzes business invoices.
# This is the first small step of the AI Document Intelligence Hub.

# This imports date from Python.
# We use date to check if the invoice is overdue.
from datetime import date

# This list saves many invoice texts.
# A list can store many items.
invoice_texts = [
    """
Invoice Number: INV-2026-001
Supplier: ABC Logistics
Invoice Date: 2026-06-01
Due Date: 2026-06-20
Total: 1250.00 EUR
VAT Number: IE1234567A
""",
    """
Invoice Number: INV-2026-002
Supplier: Northwind Office Supplies
Invoice Date: 2026-06-01
Due Date: 2026-05-01
Total: 980.00 EUR
VAT Number: IE7654321B
""",
    """
Invoice Number: INV-2026-003
Supplier: Contoso Industrial
Invoice Date: 2026-06-02
Due Date: 2026-06-30
Total: 8900.00 EUR
VAT Number: IE9999999C
""",
]


# This function finds invoice data in the text.
# A function is a block of code that we can use many times.
def extract_invoice_fields(text):
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
    }


# This function shows the invoice result in the terminal.
# It makes the result easy to read.
def show_result(fields, validation):
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

    # This loop reads one result at a time.
    for result in results:
        # This adds the risk score to the total.
        total_risk_score = total_risk_score + result["risk_score"]
        # This adds the invoice amount to the total amount.
        total_invoice_amount = total_invoice_amount + result["total_amount"]

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
    # This line shows the total amount of all invoices.
    print(f"total_invoice_amount: {total_invoice_amount}")


# This function controls the program flow.
# It processes many invoices, one by one.
def main():
    # This list saves all validation results.
    # Later, we use this list to create a summary.
    all_results = []

    # This loop reads one invoice text at a time.
    for invoice_text in invoice_texts:
        # This line extracts fields from one invoice text.
        invoice_fields = extract_invoice_fields(invoice_text)

        # This line validates the extracted fields.
        validation_result = validate_invoice(invoice_fields)

        # This line saves the result in the all_results list.
        all_results.append(validation_result)

        # This line shows the final result.
        show_result(invoice_fields, validation_result)

        # This line separates one invoice result from the next.
        print()
        print("=" * 50)
        print()

    # This line shows the final summary report.
    show_summary(all_results)


# This condition starts the program.
# It runs main() only when we run this file directly.
if __name__ == "__main__":
    main()
