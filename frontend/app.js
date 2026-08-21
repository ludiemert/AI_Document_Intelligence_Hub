// This file controls the dashboard data.
// It reads API data, filters invoices, and updates the HTML page.

// This variable saves all invoices from the Flask API.
let allInvoices = [];

// These variables save Chart.js charts.
// We use them to update charts without duplicates.
let statusChart = null;
let riskScoreChart = null;
let yearlyAmountChart = null;
let yearlyRiskChart = null;
let monthlyStatusChart = null;

// This formats money in European style.
// Example: 44300 becomes 44.300,00
function formatMoney(value) {
  return Number(value || 0).toLocaleString("de-DE", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

// This updates one HTML element by id.
function updateText(elementId, value) {
  const element = document.getElementById(elementId);

  if (element) {
    element.textContent = value;
  }
}

// This loads invoice data from the Flask API.
async function loadInvoiceResults() {
  const response = await fetch("/api/invoices");
  allInvoices = await response.json();
}

// This gets the invoice year.
// Example: 2026-06-01 becomes 2026.
function getInvoiceYear(invoice) {
  return invoice.invoice_date.slice(0, 4);
}

// This gets the invoice month.
// Example: 2026-06-01 becomes 6.
function getInvoiceMonth(invoice) {
  return String(Number(invoice.invoice_date.slice(5, 7)));
}

// This fills the year filter.
function fillYearFilter() {
  const yearFilter = document.getElementById("year-filter");

  if (!yearFilter) {
    return;
  }

  const years = [...new Set(allInvoices.map(getInvoiceYear))].sort();

  yearFilter.innerHTML = '<option value="all">All</option>';

  years.forEach((year) => {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearFilter.appendChild(option);
  });
}

// This fills the month filter.
function fillMonthFilter() {
  const monthFilter = document.getElementById("month-filter");

  if (!monthFilter) {
    return;
  }

  const months = [...new Set(allInvoices.map(getInvoiceMonth))].sort(
    (firstMonth, secondMonth) => Number(firstMonth) - Number(secondMonth),
  );

  monthFilter.innerHTML = '<option value="all">All</option>';

  months.forEach((month) => {
    const option = document.createElement("option");
    option.value = month;
    option.textContent = month;
    monthFilter.appendChild(option);
  });
}

// This returns invoices based on selected year and month.
function getFilteredInvoices() {
  const selectedYear = document.getElementById("year-filter").value;
  const selectedMonth = document.getElementById("month-filter").value;

  return allInvoices.filter((invoice) => {
    const invoiceYear = getInvoiceYear(invoice);
    const invoiceMonth = getInvoiceMonth(invoice);

    const yearMatches = selectedYear === "all" || invoiceYear === selectedYear;
    const monthMatches =
      selectedMonth === "all" || invoiceMonth === selectedMonth;

    return yearMatches && monthMatches;
  });
}

// This calculates dashboard metrics.
function calculateMetrics(invoices) {
  const totalInvoices = invoices.length;

  const approved = invoices.filter(
    (invoice) => invoice.status === "approved",
  ).length;

  const needsReview = invoices.filter(
    (invoice) => invoice.status === "needs_review",
  ).length;

  const highRisk = invoices.filter(
    (invoice) => invoice.status === "high_risk",
  ).length;

  const totalAmount = invoices.reduce(
    (sum, invoice) => sum + Number(invoice.total_amount || 0),
    0,
  );

  const totalRisk = invoices.reduce(
    (sum, invoice) => sum + Number(invoice.risk_score || 0),
    0,
  );

  const averageRisk = totalInvoices > 0 ? totalRisk / totalInvoices : 0;

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

// This updates the Status Counts chart.
function updateStatusChart(metrics) {
  const chartCanvas = document.getElementById("status-chart");

  if (!chartCanvas) {
    return;
  }

  if (statusChart) {
    statusChart.destroy();
  }

  statusChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels: ["Approved", "Needs Review", "High Risk"],
      datasets: [
        {
          label: "Number of Invoices",
          data: [metrics.approved, metrics.needsReview, metrics.highRisk],
          backgroundColor: ["#16a34a", "#f59e0b", "#dc2626"],
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

// This updates the Risk Score chart.
function updateRiskScoreChart(invoices) {
  const chartCanvas = document.getElementById("risk-score-chart");

  if (!chartCanvas) {
    return;
  }

  if (riskScoreChart) {
    riskScoreChart.destroy();
  }

  riskScoreChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels: invoices.map((invoice) => invoice.invoice_number),
      datasets: [
        {
          label: "Risk Score",
          data: invoices.map((invoice) => Number(invoice.risk_score || 0)),
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

// This updates the Monthly Status chart.
function updateMonthlyStatusChart(invoices) {
  const chartCanvas = document.getElementById("monthly-status-chart");

  if (!chartCanvas) {
    return;
  }

  const monthlyData = {};

  invoices.forEach((invoice) => {
    const year = getInvoiceYear(invoice);
    const month = String(getInvoiceMonth(invoice)).padStart(2, "0");
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

  const labels = Object.keys(monthlyData).sort();
  const approvedValues = labels.map((month) => monthlyData[month].approved);
  const needsReviewValues = labels.map(
    (month) => monthlyData[month].needs_review,
  );
  const highRiskValues = labels.map((month) => monthlyData[month].high_risk);

  if (monthlyStatusChart) {
    monthlyStatusChart.destroy();
  }

  monthlyStatusChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels,
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

// This updates the Yearly Amount chart.
function updateYearlyAmountChart(invoices) {
  const chartCanvas = document.getElementById("yearly-amount-chart");

  if (!chartCanvas) {
    return;
  }

  const amountByYear = {};

  invoices.forEach((invoice) => {
    const year = getInvoiceYear(invoice);

    if (!amountByYear[year]) {
      amountByYear[year] = 0;
    }

    amountByYear[year] += Number(invoice.total_amount || 0);
  });

  const labels = Object.keys(amountByYear).sort();
  const values = labels.map((year) => amountByYear[year]);

  if (yearlyAmountChart) {
    yearlyAmountChart.destroy();
  }

  yearlyAmountChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels,
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
        tooltip: {
          callbacks: {
            label: (context) => `${formatMoney(context.raw)} EUR`,
          },
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
          ticks: {
            callback: (value) => formatMoney(value),
          },
          title: {
            display: true,
            text: "Total Invoice Amount",
          },
        },
      },
    },
  });
}

// This updates the Yearly Average Risk chart.
function updateYearlyRiskChart(invoices) {
  const chartCanvas = document.getElementById("yearly-risk-chart");

  if (!chartCanvas) {
    return;
  }

  const riskByYear = {};

  invoices.forEach((invoice) => {
    const year = getInvoiceYear(invoice);

    if (!riskByYear[year]) {
      riskByYear[year] = [];
    }

    riskByYear[year].push(Number(invoice.risk_score || 0));
  });

  const labels = Object.keys(riskByYear).sort();
  const values = labels.map((year) => {
    const scores = riskByYear[year];
    const total = scores.reduce((sum, score) => sum + score, 0);
    return total / scores.length;
  });

  if (yearlyRiskChart) {
    yearlyRiskChart.destroy();
  }

  yearlyRiskChart = new Chart(chartCanvas, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Average Risk Score",
          data: values,
          backgroundColor: "#dc2626",
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
          suggestedMax: 35,
          title: {
            display: true,
            text: "Average Risk Score",
          },
        },
      },
    },
  });
}

// This creates a simple business recommendation.
function createFilteredRecommendation(metrics) {
  if (metrics.totalInvoices === 0) {
    return "No invoices found for this filter.";
  }

  if (metrics.needsReviewPercentage > 50) {
    return "More than 50% of invoices need review. The finance team should check invoice quality and supplier deadlines.";
  }

  if (metrics.averageRisk > 30) {
    return "The average risk score is high. The company should review high-risk invoices first.";
  }

  return "Invoice risk is under control. The team should continue monitoring the process.";
}

// This creates a yearly recommendation.
function createFilteredYearlyRecommendation(invoices, metrics) {
  if (invoices.length === 0) {
    return "No yearly data found for this filter.";
  }

  const selectedYear = document.getElementById("year-filter").value;

  if (selectedYear !== "all") {
    return `Selected year ${selectedYear} has an average risk score of ${metrics.averageRisk.toFixed(2)}.`;
  }

  return "All years are selected. Use the year filter to see a specific yearly recommendation.";
}

// This updates risk alerts.
function updateRiskAlerts(invoices) {
  const alertsList = document.getElementById("risk-alerts-list");

  if (!alertsList) {
    return;
  }

  alertsList.innerHTML = "";

  const reviewInvoices = invoices.filter(
    (invoice) => invoice.status === "needs_review",
  );

  const highAmountInvoices = invoices.filter(
    (invoice) => Number(invoice.total_amount || 0) > 5000,
  );

  if (reviewInvoices.length > 0) {
    const alert = document.createElement("p");
    alert.className = "risk-alert warning";
    alert.textContent = `${reviewInvoices.length} invoice(s) need review. Finance team should check these documents.`;
    alertsList.appendChild(alert);
  }

  highAmountInvoices.forEach((invoice) => {
    const alert = document.createElement("p");
    alert.className = "risk-alert danger";
    alert.textContent = `High amount invoice detected: ${invoice.invoice_number} (${formatMoney(invoice.total_amount)} ${invoice.currency}).`;
    alertsList.appendChild(alert);
  });

  if (alertsList.innerHTML === "") {
    const alert = document.createElement("p");
    alert.className = "risk-alert safe";
    alert.textContent = "No risk alerts for this filter.";
    alertsList.appendChild(alert);
  }
}

// This updates the top risk invoice list.
function updateTopRiskInvoices(invoices) {
  const topRiskList = document.getElementById("top-risk-list");

  if (!topRiskList) {
    return;
  }

  topRiskList.innerHTML = "";

  const topInvoices = [...invoices]
    .sort((firstInvoice, secondInvoice) => {
      return Number(secondInvoice.risk_score) - Number(firstInvoice.risk_score);
    })
    .slice(0, 3);

  if (topInvoices.length === 0) {
    const emptyMessage = document.createElement("p");
    emptyMessage.className = "top-risk-empty";
    emptyMessage.textContent = "No invoices found for this filter.";
    topRiskList.appendChild(emptyMessage);
    return;
  }

  topInvoices.forEach((invoice, index) => {
    const item = document.createElement("div");
    item.className = "top-risk-item";

    item.innerHTML = `
      <span class="top-risk-rank">${index + 1}</span>

      <div class="top-risk-info">
        <strong>${invoice.invoice_number}</strong>
        <span>${invoice.supplier_name}</span>
      </div>

      <span class="top-risk-score">Risk ${invoice.risk_score}</span>
    `;

    item.addEventListener("click", () => {
      window.location.href = `/invoice/${invoice.invoice_number}`;
    });

    topRiskList.appendChild(item);
  });
}

// This updates the invoice details table.
function updateInvoiceTable(invoices) {
  const tableBody = document.getElementById("invoice-table-body");

  if (!tableBody) {
    return;
  }

  tableBody.innerHTML = "";

  if (invoices.length === 0) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td colspan="7">No invoices found for this filter.</td>
    `;
    tableBody.appendChild(row);
    return;
  }

  invoices.forEach((invoice) => {
    const row = document.createElement("tr");
    row.className = `invoice-row ${invoice.status}`;

    row.innerHTML = `
      <td>${invoice.invoice_number}</td>
      <td>${invoice.supplier_name}</td>
      <td>${invoice.invoice_date}</td>
      <td>${formatMoney(invoice.total_amount)} ${invoice.currency}</td>
      <td>
        <span class="status-badge ${invoice.status}">
          ${invoice.status}
        </span>
      </td>
      <td>
        <span class="source-badge ${invoice.source_type}">
          ${invoice.source_type || "unknown"}
        </span>
      </td>
      <td>${invoice.risk_score}</td>
    `;

    row.addEventListener("click", () => {
      window.location.href = `/invoice/${invoice.invoice_number}`;
    });

    tableBody.appendChild(row);
  });
}

// This updates all dashboard cards, charts, alerts, and tables.
function updateDashboardFromFilters() {
  const filteredInvoices = getFilteredInvoices();
  const metrics = calculateMetrics(filteredInvoices);

  updateText("total-invoices", metrics.totalInvoices);
  updateText("approved", metrics.approved);
  updateText("needs-review", metrics.needsReview);
  updateText("high-risk", metrics.highRisk);
  updateText("average-risk", metrics.averageRisk.toFixed(2));
  updateText(
    "total-amount",
    `${formatMoney(metrics.totalAmount)} ${metrics.currency}`,
  );
  updateText(
    "needs-review-percentage",
    `${metrics.needsReviewPercentage.toFixed(2)}%`,
  );

  updateText("general-recommendation", createFilteredRecommendation(metrics));
  updateText(
    "yearly-recommendation",
    createFilteredYearlyRecommendation(filteredInvoices, metrics),
  );

  updateStatusChart(metrics);
  updateRiskScoreChart(filteredInvoices);
  updateMonthlyStatusChart(filteredInvoices);
  updateYearlyAmountChart(filteredInvoices);
  updateYearlyRiskChart(filteredInvoices);
  updateRiskAlerts(filteredInvoices);
  updateTopRiskInvoices(filteredInvoices);
  updateInvoiceTable(filteredInvoices);
}

// This changes the dashboard view.
function setDashboardView(selectedView) {
  const sections = document.querySelectorAll(".dashboard-section");

  sections.forEach((section) => {
    const shouldShow = section.classList.contains(`${selectedView}-section`);
    section.classList.toggle("hidden", !shouldShow);
  });

  const buttons = document.querySelectorAll(".view-button");

  buttons.forEach((button) => {
    const isActive = button.dataset.view === selectedView;
    button.classList.toggle("active", isActive);
  });
}

// This connects click events to view buttons.
function setupViewControls() {
  const buttons = document.querySelectorAll(".view-button");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      setDashboardView(button.dataset.view);
    });
  });
}

// This connects change events to filters.
function setupFilters() {
  document
    .getElementById("year-filter")
    .addEventListener("change", updateDashboardFromFilters);

  document
    .getElementById("month-filter")
    .addEventListener("change", updateDashboardFromFilters);
}

// This starts the dashboard.
async function startDashboard() {
  await loadInvoiceResults();

  fillYearFilter();
  fillMonthFilter();
  setupViewControls();
  setupFilters();
  setDashboardView("general");
  updateDashboardFromFilters();
}

// This closes the message box.
function closeMessage() {
  const messageOverlay = document.getElementById("message-overlay");

  if (messageOverlay) {
    messageOverlay.style.display = "none";
  }
}

// This starts the dashboard when the page opens.
startDashboard();
