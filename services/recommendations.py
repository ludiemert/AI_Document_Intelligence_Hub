# This file creates business recommendations.
# Recommendations help the company decide what to do.


# This function creates a simple business recommendation.
# It uses business metrics to choose a message.
def create_recommendation(metrics):
    """Create a simple business recommendation."""
    # This gets the needs review percentage.
    needs_review_percentage = metrics["needs_review_percentage"]

    # This gets the average risk score.
    average_risk_score = metrics["average_risk_score"]

    # This creates a recommendation based on business rules.
    if needs_review_percentage > 50:
        recommendation = (
            "More than 50% of invoices need review. "
            "The finance team should check invoice quality and supplier deadlines."
        )
    elif average_risk_score > 30:
        recommendation = (
            "The average risk score is high. "
            "The company should review high-risk invoices first."
        )
    else:
        recommendation = (
            "Invoice risk is under control. "
            "The team should continue monitoring the process."
        )

    print()
    print("BUSINESS RECOMMENDATION")
    print("-----------------------")
    print(f"needs_review_percentage: {needs_review_percentage}%")
    print(f"recommendation: {recommendation}")

    # This returns the recommendation text.
    return recommendation

    # This function creates a recommendation based on yearly risk.


# It helps the company see which year needs more attention.
def create_yearly_recommendation(yearly_summary):
    """Create a recommendation based on yearly risk."""
    # This checks if the yearly summary is empty.
    # If it is empty, the app returns a safe message.
    if yearly_summary.empty:
        return "No yearly data available."

    # This finds the row with the highest average risk score.
    highest_risk_row = yearly_summary.loc[yearly_summary["average_risk_score"].idxmax()]

    # This gets the year with the highest risk.
    highest_risk_year = int(highest_risk_row["invoice_year"])

    # This gets the highest average risk score.
    highest_risk_score = float(highest_risk_row["average_risk_score"])

    # This creates a recommendation message.
    if highest_risk_score == 0:
        yearly_recommendation = (
            "All years have zero average risk. "
            "The company should continue monitoring invoices."
        )
    else:
        yearly_recommendation = (
            f"{highest_risk_year} has the highest average risk score "
            f"({highest_risk_score}). Review invoices from this year first."
        )

    print()
    print("YEARLY RECOMMENDATION")
    print("---------------------")
    print(f"recommendation: {yearly_recommendation}")

    # This returns the yearly recommendation text.
    return yearly_recommendation
