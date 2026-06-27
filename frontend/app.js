// This file controls the dashboard data.
// It reads JSON files and updates the HTML page.

// This function updates one HTML element by id.
// It changes the text inside the element.
function updateText(elementId, value) {
  // This finds the HTML element by id.
  const element = document.getElementById(elementId);

  // This checks if the element exists.
  if (element) {
    // This updates the text on the page.
    element.textContent = value;
  }
}

// This function loads the summary JSON file.
// It updates the metric cards on the dashboard.
async function loadSummaryData() {
  // This reads the summary JSON created by Python.
  const response = await fetch("../reports/invoice_summary.json");

  // This converts the response to JavaScript data.
  const summary = await response.json();

  // This updates total invoices.
  updateText("total-invoices", summary.total_invoices);

  // This updates approved invoices.
  updateText("approved", summary.approved);

  // This updates invoices that need review.
  updateText("needs-review", summary.needs_review);

  // This updates high risk invoices.
  updateText("high-risk", summary.high_risk);

  // This updates average risk score.
  updateText("average-risk", summary.average_risk_score);

  // This updates total invoice amount with currency.
  updateText(
    "total-amount",
    `${summary.total_invoice_amount.toFixed(2)} ${summary.currency}`,
  );

  // This updates needs review percentage.
  updateText("needs-review-percentage", `${summary.needs_review_percentage}%`);
}

// This function loads the recommendations JSON file.
// It updates the recommendation cards on the dashboard.
async function loadRecommendations() {
  // This reads the recommendations JSON created by Python.
  const response = await fetch("../reports/business_recommendations.json");

  // This converts the response to JavaScript data.
  const recommendations = await response.json();

  // This updates the general recommendation.
  updateText("general-recommendation", recommendations.general_recommendation);

  // This updates the yearly recommendation.
  updateText("yearly-recommendation", recommendations.yearly_recommendation);
}

// This function starts the dashboard.
// It loads summary data and recommendations.
async function startDashboard() {
  // This loads metric cards.
  await loadSummaryData();

  // This loads recommendation cards.
  await loadRecommendations();
}

// This function changes the dashboard view.
// It shows general, monthly, or yearly sections.
function setDashboardView(selectedView) {
  // This gets all dashboard sections.
  const sections = document.querySelectorAll(".dashboard-section");

  // This reads one section at a time.
  sections.forEach((section) => {
    // This checks if the section belongs to the selected view.
    const shouldShow = section.classList.contains(`${selectedView}-section`);

    // This hides or shows the section.
    section.classList.toggle("hidden", !shouldShow);
  });

  // This gets all view buttons.
  const buttons = document.querySelectorAll(".view-button");

  // This updates the active button.
  buttons.forEach((button) => {
    // This checks if this button is the selected button.
    const isActive = button.dataset.view === selectedView;

    // This adds or removes the active class.
    button.classList.toggle("active", isActive);
  });
}

// This function connects click events to view buttons.
function setupViewControls() {
  // This gets all view buttons.
  const buttons = document.querySelectorAll(".view-button");

  // This adds a click event to each button.
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      // This gets the view name from the button.
      const selectedView = button.dataset.view;

      // This changes the dashboard view.
      setDashboardView(selectedView);
    });
  });
}

// This starts the view controls.
setupViewControls();

// This shows the general view first.
setDashboardView("general");

// This starts the dashboard when the page opens.
startDashboard();
