// This file controls the dashboard data.
// It reads JSON files, filters data, and updates the HTML page.

// This variable saves all invoices from JSON.
let allInvoices = [];

// This function updates one HTML element by id.
function updateText(elementId, value) {
  // This finds the HTML element by id.
  const element = document.getElementById(elementId);

  // This checks if the element exists.
  if (element) {
    // This updates the text on the page.
    element.textContent = value;
  }
}

// This function loads invoice details from JSON.
// This JSON is created by Python.
async function loadInvoiceResults() {
  // This reads the detailed invoice JSON file.
  const response = await fetch("../reports/invoice_results.json");

  // This converts JSON into JavaScript data.
  allInvoices = await response.json();
}

// This function gets the year from invoice_date.
// Example: 2026-06-01 becomes 2026.
function getInvoiceYear(invoice) {
  return invoice.invoice_date.slice(0, 4);
}

// This function gets the month from invoice_date.
// Example: 2026-06-01 becomes 6.
function getInvoiceMonth(invoice) {
  return String(Number(invoice.invoice_date.slice(5, 7)));
}

// This function fills the year filter.
function fillYearFilter() {
  // This finds the year select.
  const yearFilter = document.getElementById("year-filter");

  // This gets unique years from invoices.
  const years = [...new Set(allInvoices.map(getInvoiceYear))];

  // This adds one option for each year.
  years.forEach((year) => {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearFilter.appendChild(option);
  });
}

// This function fills the month filter.
function fillMonthFilter() {
  // This finds the month select.
  const monthFilter = document.getElementById("month-filter");

  // This gets unique months from invoices.
  const months = [...new Set(allInvoices.map(getInvoiceMonth))];

  // This sorts months from small to big.
  months.sort((a, b) => Number(a) - Number(b));

  // This adds one option for each month.
  months.forEach((month) => {
    const option = document.createElement("option");
    option.value = month;
    option.textContent = month;
    monthFilter.appendChild(option);
  });
}

// This function returns invoices based on selected year and month.
function getFilteredInvoices() {
  // This gets selected year.
  const selectedYear = document.getElementById("year-filter").value;

  // This gets selected month.
  const selectedMonth = document.getElementById("month-filter").value;

  // This filters invoices.
  return allInvoices.filter((invoice) => {
    const invoiceYear = getInvoiceYear(invoice);
    const invoiceMonth = getInvoiceMonth(invoice);

    const yearMatches = selectedYear === "all" || invoiceYear === selectedYear;
    const monthMatches =
      selectedMonth === "all" || invoiceMonth === selectedMonth;

    return yearMatches && monthMatches;
  });
}

// This function calculates dashboard metrics.
function calculateMetrics(invoices) {
  // This counts total invoices.
  const totalInvoices = invoices.length;

  // This counts approved invoices.
  const approved = invoices.filter(
    (invoice) => invoice.status === "approved",
  ).length;

  // This counts invoices that need review.
  const needsReview = invoices.filter(
    (invoice) => invoice.status === "needs_review",
  ).length;

  // This counts high risk invoices.
  const highRisk = invoices.filter(
    (invoice) => invoice.status === "high_risk",
  ).length;

  // This sums total invoice amount.
  const totalAmount = invoices.reduce(
    (sum, invoice) => sum + Number(invoice.total_amount),
    0,
  );

  // This sums risk scores.
  const totalRisk = invoices.reduce(
    (sum, invoice) => sum + Number(invoice.risk_score),
    0,
  );

  // This calculates average risk.
  const averageRisk = totalInvoices > 0 ? totalRisk / totalInvoices : 0;

  // This calculates needs review percentage.
  const needsReviewPercentage =
    totalInvoices > 0 ? (needsReview / totalInvoices) * 100 : 0;

  return {
    totalInvoices,
    approved,
    needsReview,
    highRisk,
    totalAmount,
    averageRisk,
    needsReviewPercentage,
    currency: invoices[0]?.currency || "EUR",
  };
}

// This function creates a simple recommendation from filtered data.
function createFilteredRecommendation(metrics) {
  // This checks if there is no data.
  if (metrics.totalInvoices === 0) {
    return "No invoices found for this filter.";
  }

  // This creates a recommendation based on needs review percentage.
  if (metrics.needsReviewPercentage > 50) {
    return "More than 50% of invoices need review. The finance team should check invoice quality and supplier deadlines.";
  }

  // This creates a recommendation based on average risk.
  if (metrics.averageRisk > 30) {
    return "The average risk score is high. The company should review high-risk invoices first.";
  }

  return "Invoice risk is under control. The team should continue monitoring the process.";
}

// This function creates a yearly recommendation from filtered invoices.
// It helps explain the selected year or period.
function createFilteredYearlyRecommendation(invoices, metrics) {
  // This checks if there is no data.
  if (invoices.length === 0) {
    return "No yearly data found for this filter.";
  }

  // This gets the selected year.
  const selectedYear = document.getElementById("year-filter").value;

  // This gets the selected month.
  const selectedMonth = document.getElementById("month-filter").value;

  // This creates a message for one selected year.
  if (selectedYear !== "all") {
    return `Selected year ${selectedYear} has an average risk score of ${metrics.averageRisk.toFixed(2)}.`;
  }

  // This creates a message for all years.
  return "All years are selected. Use the year filter to see a specific yearly recommendation.";
}

// This function updates metric cards and recommendation text.
function updateDashboardFromFilters() {
  // This gets filtered invoices.
  const filteredInvoices = getFilteredInvoices();

  // This calculates metrics from filtered invoices.
  const metrics = calculateMetrics(filteredInvoices);

  // This updates metric cards.
  updateText("total-invoices", metrics.totalInvoices);
  updateText("approved", metrics.approved);
  updateText("needs-review", metrics.needsReview);
  updateText("high-risk", metrics.highRisk);
  updateText("average-risk", metrics.averageRisk.toFixed(2));
  updateText(
    "total-amount",
    `${metrics.totalAmount.toFixed(2)} ${metrics.currency}`,
  );
  updateText(
    "needs-review-percentage",
    `${metrics.needsReviewPercentage.toFixed(2)}%`,
  );

  // This updates recommendation text.
  updateText("general-recommendation", createFilteredRecommendation(metrics));

  // This updates yearly recommendation text.
  updateText(
    "yearly-recommendation",
    createFilteredYearlyRecommendation(filteredInvoices, metrics),
  );
}

// This function changes the dashboard view.
function setDashboardView(selectedView) {
  // This gets all dashboard sections.
  const sections = document.querySelectorAll(".dashboard-section");

  // This shows or hides sections.
  sections.forEach((section) => {
    const shouldShow = section.classList.contains(`${selectedView}-section`);
    section.classList.toggle("hidden", !shouldShow);
  });

  // This gets all view buttons.
  const buttons = document.querySelectorAll(".view-button");

  // This updates the active button.
  buttons.forEach((button) => {
    const isActive = button.dataset.view === selectedView;
    button.classList.toggle("active", isActive);
  });
}

// This function connects click events to view buttons.
function setupViewControls() {
  const buttons = document.querySelectorAll(".view-button");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      setDashboardView(button.dataset.view);
    });
  });
}

// This function connects change events to filters.
function setupFilters() {
  // This updates dashboard when year changes.
  document
    .getElementById("year-filter")
    .addEventListener("change", updateDashboardFromFilters);

  // This updates dashboard when month changes.
  document
    .getElementById("month-filter")
    .addEventListener("change", updateDashboardFromFilters);
}

// This function starts the dashboard.
async function startDashboard() {
  // This loads detailed invoice data.
  await loadInvoiceResults();

  // This fills filters from invoice data.
  fillYearFilter();
  fillMonthFilter();

  // This connects buttons and filters.
  setupViewControls();
  setupFilters();

  // This shows the general view first.
  setDashboardView("general");

  // This updates dashboard with all data first.
  updateDashboardFromFilters();
}

// This starts the dashboard when the page opens.
startDashboard();
