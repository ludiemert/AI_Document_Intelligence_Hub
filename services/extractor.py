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

            # This checks if the currency exists.
            # If it exists, Python saves it.
            if len(total_parts) > 1:
                fields["currency"] = total_parts[1]

        # This condition checks if the line starts with "VAT Number:".
        # If it is true, Python saves the VAT number.
        if line.startswith("VAT Number:"):
            fields["vat_number"] = line.replace("VAT Number:", "").strip()

    # This returns the dictionary with all invoice fields.
    # Return sends the result back to the code.
    return fields
