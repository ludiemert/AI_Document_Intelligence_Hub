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
    # This checks if there are no results.
    # If there are no results, the summary stops safely.
    if not results:
        print("No results to summarize.")
        return

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
