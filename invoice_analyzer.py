# This project analyzes business invoices.
# This is the first small step of the AI Document Intelligence Hub.

# This variable saves the invoice text.
# A variable is a name that stores a value.
invoice_text = """
Invoice Number: INV-2026-001
Supplier: ABC Logistics
Invoice Date: 2026-06-01
Due Date: 2026-06-20
Total: 1250.00 EUR
VAT Number: IE1234567A
"""


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
        # If it is true, Python saves the total amount and currency.
        if line.startswith("Total:"):
            fields["total"] = line.replace("Total:", "").strip()

        # This condition checks if the line starts with "VAT Number:".
        # If it is true, Python saves the VAT number.
        if line.startswith("VAT Number:"):
            fields["vat_number"] = line.replace("VAT Number:", "").strip()

    # This returns the dictionary with all invoice fields.
    # Return sends the result back to the code.
    return fields


# This function checks if the invoice has all important fields.
# It returns the invoice status.
def validate_invoice(fields):
    # This list has all required fields for an invoice.
    # Required means the field is important and cannot be empty.
    required_fields = [
        "invoice_number",
        "supplier_name",
        "invoice_date",
        "due_date",
        "total",
        "vat_number",
    ]

    # This list will save fields that are missing.
    # Missing means the data is not in the invoice.
    missing_fields = []

    # This loop checks one required field at a time.
    for field in required_fields:

        # This condition checks if the field is not in the dictionary.
        # If the field is missing, Python saves it in missing_fields.
        if field not in fields or fields[field] == "":
            missing_fields.append(field)

    # If missing_fields has data, the invoice needs review.
    if missing_fields:
        return {
            "status": "needs_review",
            "missing_fields": missing_fields,
        }

    # If no field is missing, the invoice is approved.
    return {
        "status": "approved",
        "missing_fields": [],
    }


# This line calls the extract function.
# The result is saved in invoice_fields.
invoice_fields = extract_invoice_fields(invoice_text)

# This line calls the validate function.
# The result is saved in validation_result.
validation_result = validate_invoice(invoice_fields)

# This title makes the terminal result easier to read.
print("INVOICE FIELDS")
print("--------------")

# This loop shows one invoice field per line.
for field_name, field_value in invoice_fields.items():
    print(f"{field_name}: {field_value}")

# This empty print creates a blank line.
print()

# This title shows the validation result.
print("VALIDATION RESULT")
print("-----------------")

# This line shows the invoice status.
print(f"status: {validation_result['status']}")

# This line shows missing fields.
print(f"missing_fields: {validation_result['missing_fields']}")
