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


# This line calls the function and sends invoice_text to it.
# The result is saved in invoice_fields.
invoice_fields = extract_invoice_fields(invoice_text)

# This loop shows one invoice field per line.
# It makes the result easier to read.
for field_name, field_value in invoice_fields.items():
    print(f"{field_name}: {field_value}")
