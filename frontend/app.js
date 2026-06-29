// This file controls the dashboard data.
// It reads JSON files, filters data, and updates the HTML page.

// This variable saves all invoices from JSON.
let allInvoices = [];

// This variable saves the Status Counts chart.
// We use it to update the chart without creating duplicates.
let statusChart = null;

// This variable saves the Risk Score chart.
// We use it to update the chart without creating duplicates.
let riskScoreChart = null;

// This variable saves the Yearly Amount chart.
// We use it to update the chart without creating duplicates.
let yearlyAmountChart = null;

// This variable saves the Monthly Status chart.
// We use it to update the chart without creating duplicates.
let monthlyStatusChart = null;

function updateMonthlyStatusChart(invoices) {
  // This gets the canvas from the HTML.
  const chartCanvas = document.getElementById("monthly-status-chart");

  // This stops the function if the canvas does not exist.
  if (!chartCanvas) {
    return;
  }

  // This object saves status counts by month.
  const monthlyData = {};

  // This loops through invoices and groups data by year and month.
  invoices.forEach((invoice) => {
    const date = new Date(invoice.invoice_date);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const monthKey = `${year}-${month}`;

    if (!monthlyData[monthKey]) {
      monthlyData[monthKey] = {
        approved: 0,
        needs_review: 0,
        high_risk: 0,
      };
    }

    monthlyData[monthKey][invoice.status] += 1;
  });

  // This gets month labels for the X axis.
  const labels = Object.keys(monthlyData);

  // This gets approved values.
  const approvedValues = labels.map((month) => monthlyData[month].approved);

  // This gets needs review values.
  const needsReviewValues = labels.map(
    (month) => monthlyData[month].needs_review,
  );

  // This gets high risk values.
  const highRiskValues = labels.map((month) => monthlyData[month].high_risk);

  // This removes the old chart before creating a new one.
  if (monthlyStatusChart) {
    monthlyStatusChart.destroy();
  }

  // This creates the Monthly Status chart.
  monthlyStatusChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Approved",
          data: approvedValues,
          backgroundColor: "#16a34a",
          borderRadius: 6,
        },
        {
          label: "Needs Review",
          data: needsReviewValues,
          backgroundColor: "#f59e0b",
          borderRadius: 6,
        },
        {
          label: "High Risk",
          data: highRiskValues,
          backgroundColor: "#dc2626",
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: "Year and Month",
          },
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Number of Invoices",
          },
        },
      },
    },
  });
}

function updateYearlyAmountChart(invoices) {
  // This gets the canvas from the HTML.
  const chartCanvas = document.getElementById("yearly-amount-chart");

  // This stops the function if the canvas does not exist.
  if (!chartCanvas) {
    return;
  }

  // This object will save total amount by year.
  const amountByYear = {};

  // This loops through invoices and groups amounts by year.
  invoices.forEach((invoice) => {
    const year = new Date(invoice.invoice_date).getFullYear();
    const amount = Number(invoice.total_amount);

    if (!amountByYear[year]) {
      amountByYear[year] = 0;
    }

    amountByYear[year] += amount;
  });

  // This gets the years for the X axis.
  const labels = Object.keys(amountByYear);

  // This gets the total amounts for the Y axis.
  const values = Object.values(amountByYear);

  // This removes the old chart before creating a new one.
  if (yearlyAmountChart) {
    yearlyAmountChart.destroy();
  }

  // This creates the Yearly Amount chart.
  yearlyAmountChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Total Amount",
          data: values,
          backgroundColor: "#0f766e",
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Year",
          },
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Total Invoice Amount",
          },
        },
      },
    },
  });
}

function updateRiskScoreChart(invoices) {
  // This gets the canvas from the HTML.
  const chartCanvas = document.getElementById("risk-score-chart");

  // This stops the function if the canvas does not exist.
  if (!chartCanvas) {
    return;
  }

  // This gets invoice numbers for the X axis.
  const labels = invoices.map((invoice) => invoice.invoice_number);

  // This gets risk scores for the Y axis.
  const values = invoices.map((invoice) => Number(invoice.risk_score));

  // This removes the old chart before creating a new one.
  if (riskScoreChart) {
    riskScoreChart.destroy();
  }

  // This creates the Risk Score chart.
  riskScoreChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Risk Score",
          data: values,
          backgroundColor: "#2563eb",
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Invoice Number",
          },
        },
        y: {
          beginAtZero: true,
          suggestedMax: 35,
          title: {
            display: true,
            text: "Risk Score",
          },
        },
      },
    },
  });
}

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

// This function updates the Status Counts chart with Chart.js.
// It shows approved, needs review, and high risk invoices.
function updateStatusChart(metrics) {
  // This finds the chart canvas.
  const chartCanvas = document.getElementById("status-chart");

  // This checks if the canvas exists.
  if (!chartCanvas) {
    return;
  }

  // This creates chart labels.
  const labels = ["Approved", "Needs Review", "High Risk"];

  // This creates chart values.
  const values = [metrics.approved, metrics.needsReview, metrics.highRisk];

  // This creates chart colors.
  const colors = ["#16a34a", "#f59e0b", "#dc2626"];

  // This destroys the old chart before creating a new one.
  // This avoids duplicate charts.
  if (statusChart) {
    statusChart.destroy();
  }

  // This creates the new Chart.js bar chart.
  statusChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Number of Invoices",
          data: values,
          backgroundColor: colors,
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          enabled: true,
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Status",
          },
        },
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0,
          },
          title: {
            display: true,
            text: "Number of Invoices",
          },
        },
      },
    },
  });
}

// This function updates the dynamic status chart.
// It shows approved, needs review, and high risk counts.
function updateStatusDynamicChart(metrics) {
  // This finds the chart container.
  const chartContainer = document.getElementById("status-dynamic-chart");

  // This checks if the chart container exists.
  if (!chartContainer) {
    return;
  }

  // This creates chart data.
  const chartData = [
    {
      label: "Approved",
      value: metrics.approved,
      className: "approved",
    },
    {
      label: "Needs Review",
      value: metrics.needsReview,
      className: "needs-review",
    },
    {
      label: "High Risk",
      value: metrics.highRisk,
      className: "high-risk",
    },
  ];

  // This finds the biggest value.
  // It helps calculate bar width.
  const maxValue = Math.max(...chartData.map((item) => item.value), 1);

  // This clears the old chart.
  chartContainer.innerHTML = "";

  // This creates one bar for each status.
  chartData.forEach((item) => {
    // This calculates the bar width percentage.
    const widthPercentage = (item.value / maxValue) * 100;

    // This creates one row.
    const row = document.createElement("div");
    row.className = "dynamic-bar-row";

    // This creates the label.
    const label = document.createElement("span");
    label.className = "dynamic-bar-label";
    label.textContent = item.label;

    // This creates the bar track.
    const track = document.createElement("div");
    track.className = "dynamic-bar-track";

    // This creates the colored bar.
    const fill = document.createElement("div");
    fill.className = `dynamic-bar-fill ${item.className}`;
    fill.style.width = `${widthPercentage}%`;

    // This creates the number value.
    const value = document.createElement("span");
    value.className = "dynamic-bar-value";
    value.textContent = item.value;

    // This puts the fill inside the track.
    track.appendChild(fill);

    // This puts all parts inside the row.
    row.appendChild(label);
    row.appendChild(track);
    row.appendChild(value);

    // This puts the row inside the chart.
    chartContainer.appendChild(row);
  });
}

// This function updates the dynamic risk score chart.
// It shows one bar for each filtered invoice.
function updateRiskDynamicChart(invoices) {
  // This finds the chart container.
  const chartContainer = document.getElementById("risk-dynamic-chart");

  // This checks if the chart container exists.
  if (!chartContainer) {
    return;
  }

  // This clears the old chart.
  chartContainer.innerHTML = "";

  // This checks if there are no invoices.
  if (invoices.length === 0) {
    const emptyMessage = document.createElement("p");
    emptyMessage.className = "dynamic-empty";
    emptyMessage.textContent = "No invoices found for this filter.";
    chartContainer.appendChild(emptyMessage);
    return;
  }

  // This finds the biggest risk score.
  // It helps calculate bar width.
  const maxRisk = Math.max(
    ...invoices.map((invoice) => Number(invoice.risk_score)),
    1,
  );

  // This creates one bar for each invoice.
  invoices.forEach((invoice) => {
    // This gets the risk score as a number.
    const riskScore = Number(invoice.risk_score);

    // This calculates the bar width percentage.
    const widthPercentage = (riskScore / maxRisk) * 100;

    // This creates one chart row.
    const row = document.createElement("div");
    row.className = "dynamic-bar-row";

    // This creates the invoice label.
    const label = document.createElement("span");
    label.className = "dynamic-bar-label";
    label.textContent = invoice.invoice_number;

    // This creates the bar track.
    const track = document.createElement("div");
    track.className = "dynamic-bar-track";

    // This creates the colored risk bar.
    const fill = document.createElement("div");
    fill.className = "dynamic-bar-fill risk-score";
    fill.style.width = `${widthPercentage}%`;

    // This creates the risk number.
    const value = document.createElement("span");
    value.className = "dynamic-bar-value";
    value.textContent = riskScore;

    // This puts the fill inside the track.
    track.appendChild(fill);

    // This puts all parts inside the row.
    row.appendChild(label);
    row.appendChild(track);
    row.appendChild(value);

    // This puts the row inside the chart.
    chartContainer.appendChild(row);
  });
}

// This function updates the dynamic yearly amount chart.
// It groups filtered invoices by year.
function updateYearlyAmountDynamicChart(invoices) {
  // This finds the chart container.
  const chartContainer = document.getElementById("yearly-amount-dynamic-chart");

  // This checks if the chart container exists.
  if (!chartContainer) {
    return;
  }

  // This clears the old chart.
  chartContainer.innerHTML = "";

  // This checks if there are no invoices.
  if (invoices.length === 0) {
    const emptyMessage = document.createElement("p");
    emptyMessage.className = "dynamic-empty";
    emptyMessage.textContent = "No invoices found for this filter.";
    chartContainer.appendChild(emptyMessage);
    return;
  }

  // This object will save total amount by year.
  const amountByYear = {};

  // This reads one invoice at a time.
  invoices.forEach((invoice) => {
    // This gets the invoice year.
    const year = getInvoiceYear(invoice);

    // This creates the year key if it does not exist.
    if (!amountByYear[year]) {
      amountByYear[year] = 0;
    }

    // This adds the invoice amount to the year total.
    amountByYear[year] += Number(invoice.total_amount);
  });

  // This converts the object into a list.
  const chartData = Object.entries(amountByYear).map(([year, amount]) => ({
    label: year,
    value: amount,
  }));

  // This finds the biggest amount.
  const maxValue = Math.max(...chartData.map((item) => item.value), 1);

  // This creates one bar for each year.
  chartData.forEach((item) => {
    // This calculates the bar width percentage.
    const widthPercentage = (item.value / maxValue) * 100;

    // This creates one chart row.
    const row = document.createElement("div");
    row.className = "dynamic-bar-row";

    // This creates the year label.
    const label = document.createElement("span");
    label.className = "dynamic-bar-label";
    label.textContent = item.label;

    // This creates the bar track.
    const track = document.createElement("div");
    track.className = "dynamic-bar-track";

    // This creates the colored amount bar.
    const fill = document.createElement("div");
    fill.className = "dynamic-bar-fill yearly-amount";
    fill.style.width = `${widthPercentage}%`;

    // This creates the amount value.
    const value = document.createElement("span");
    value.className = "dynamic-bar-value";
    value.textContent = item.value.toFixed(2);

    // This puts the fill inside the track.
    track.appendChild(fill);

    // This puts all parts inside the row.
    row.appendChild(label);
    row.appendChild(track);
    row.appendChild(value);

    // This puts the row inside the chart.
    chartContainer.appendChild(row);
  });
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

  // This updates the Chart.js status chart.
  updateStatusChart(metrics);

  // This updates the Risk Score chart.
  updateRiskScoreChart(filteredInvoices);

  // This updates the Yearly Amount chart.
  updateYearlyAmountChart(filteredInvoices);

  // This updates the dynamic yearly amount chart.
  updateYearlyAmountDynamicChart(filteredInvoices);

  // This updates the Monthly Status chart.
  updateMonthlyStatusChart(filteredInvoices);

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
