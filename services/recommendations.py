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
