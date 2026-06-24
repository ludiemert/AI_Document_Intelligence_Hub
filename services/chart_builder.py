# This file creates chart images.
# Charts help users understand data visually.

# This imports matplotlib.
# We use matplotlib to create charts.
import matplotlib.pyplot as plt


# This function creates a chart with invoice status counts.
# It saves the chart as a PNG image.
def create_status_chart(reports_folder, status_counts):
    """Create a chart with invoice status counts."""
    # This creates a bar chart with invoice status counts.
    status_counts.plot(kind="bar")

    # This adds a chart title.
    plt.title("Invoice Status Counts")

    # This adds a label to the x axis.
    plt.xlabel("Status")

    # This adds a label to the y axis.
    plt.ylabel("Number of Invoices")

    # This keeps the labels easy to read.
    plt.xticks(rotation=0)

    # This adjusts the chart layout.
    plt.tight_layout()

    # This saves the chart inside the reports folder.
    plt.savefig(reports_folder / "status_counts.png")

    # This clears the chart memory.
    plt.clf()

    # This message tells the user the chart was created.
    print("Chart created: status_counts.png")


# This function creates a chart with risk score by invoice.
# It saves the chart as a PNG image.
def create_risk_score_chart(reports_folder, df):
    """Create a chart with risk score by invoice."""
    # This creates a bar chart with risk score by invoice.
    plt.bar(df["invoice_number"], df["risk_score"], color="steelblue")

    # This adds a chart title.
    plt.title("Risk Score by Invoice")

    # This adds a label to the x axis.
    plt.xlabel("Invoice Number")

    # This adds a label to the y axis.
    plt.ylabel("Risk Score")

    # This adjusts the chart layout.
    plt.tight_layout()

    # This saves the chart inside the reports folder.
    plt.savefig(reports_folder / "risk_scores.png")

    # This clears the chart memory.
    plt.clf()

    # This message tells the user the chart was created.
    print("Chart created: risk_scores.png")


# This function creates a chart with monthly status counts.
# It saves the chart as a PNG image.
def create_monthly_status_chart(reports_folder, monthly_status_summary):
    """Create a chart with monthly status counts."""
    # This changes rows into columns for the chart.
    monthly_status_chart = monthly_status_summary.pivot_table(
        index=["invoice_year", "invoice_month"],
        columns="status",
        values="total_invoices",
        fill_value=0,
    )

    # This creates a bar chart from the monthly status table.
    monthly_status_chart.plot(kind="bar")

    # This adds a chart title.
    plt.title("Monthly Invoice Status Counts")

    # This adds a label to the x axis.
    plt.xlabel("Year and Month")

    # This adds a label to the y axis.
    plt.ylabel("Number of Invoices")

    # This keeps the labels easy to read.
    plt.xticks(rotation=0)

    # This adjusts the chart layout.
    plt.tight_layout()

    # This saves the chart inside the reports folder.
    plt.savefig(reports_folder / "monthly_status_counts.png")

    # This clears the chart memory.
    plt.clf()

    # This message tells the user the chart was created.
    print("Chart created: monthly_status_counts.png")

    # This function creates a chart with total invoice amount by year.


# It helps compare business volume between years.
def create_yearly_amount_chart(reports_folder, yearly_summary):
    """Create a chart with yearly invoice amount."""
    # This creates the yearly reports folder path.
    yearly_folder = reports_folder / "yearly"

    # This creates the folder if it does not exist.
    yearly_folder.mkdir(exist_ok=True)

    # This creates a bar chart with year and total amount.
    plt.bar(
        yearly_summary["invoice_year"].astype(str),
        yearly_summary["total_invoice_amount"],
        color="seagreen",
    )

    # This adds a chart title.
    plt.title("Yearly Invoice Amount")

    # This adds a label to the x axis.
    plt.xlabel("Year")

    # This adds a label to the y axis.
    plt.ylabel("Total Invoice Amount")

    # This adjusts the chart layout.
    plt.tight_layout()

    # This saves the chart inside the yearly reports folder.
    plt.savefig(yearly_folder / "yearly_invoice_amount.png")

    # This clears the chart memory.
    plt.clf()

    # This message tells the user the chart was created.
    print("Chart created: yearly_invoice_amount.png")
