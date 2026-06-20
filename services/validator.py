# This imports date from Python.
# We use date to check if the invoice is overdue.
from datetime import date


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
