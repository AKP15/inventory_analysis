import os

import matplotlib.pyplot as plt

from src.logger import get_logger

logger = get_logger(__name__)


def create_dashboard(df, table, save_dir="dashbook"):
    """Make the inventory dashboard and save it as a PNG image."""
    logger.info("Dashboard started")

    # Step 1: calculate the 5 KPI numbers
    inventory_value = (df["Stock_Quantity"] * df["Unit_Cost"]).sum()
    sales_value = (df["Stock_Quantity"] * df["Unit_Price"]).sum()
    gross_profit = sales_value - inventory_value

    critical = table[table["Inventory_Priority"] == "Critical"]
    critical_count = len(critical)
    critical_cost = critical["Reorder_Cost"].sum()

    # Step 2: create the page (2 rows x 3 charts)
    fig, axes = plt.subplots(2, 3, figsize=(20, 11))
    fig.suptitle("Inventory Dashboard", fontsize=22, fontweight="bold")

    # Step 3: KPI cards at the top
    kpis = [
        ("Total Inventory Value", f"${inventory_value:,.0f}"),
        ("Potential Sales Value", f"${sales_value:,.0f}"),
        ("Potential Gross Profit", f"${gross_profit:,.0f}"),
        ("Critical Products", f"{critical_count}"),
        ("Critical Reorder Cost", f"${critical_cost:,.0f}"),
    ]
    x_positions = [0.10, 0.30, 0.50, 0.70, 0.90]

    for x, (label, value) in zip(x_positions, kpis):
        fig.text(
            x, 0.90, f"{label}\n{value}",
            ha="center", va="center", fontsize=16, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.8", facecolor="#eef2ff", edgecolor="#6366f1"),
        )

    # Chart 1: Inventory Value by Product
    ax = axes[0, 0]
    data = table.sort_values("Inventory_Value", ascending=False)
    ax.bar(data["Product_Name"], data["Inventory_Value"].fillna(0), color="#6366f1")
    ax.set_title("Inventory Value by Product", fontweight="bold")
    ax.set_ylabel("Inventory Value ($)")
    ax.tick_params(axis="x", rotation=45)

    # Chart 2: Inventory Turnover by Product
    ax = axes[0, 1]
    data = table.sort_values("Inventory_Turnover", ascending=False)
    ax.bar(data["Product_Name"], data["Inventory_Turnover"].fillna(0), color="#0ea5e9")
    ax.set_title("Inventory Turnover by Product", fontweight="bold")
    ax.set_ylabel("Turnover")
    ax.tick_params(axis="x", rotation=45)

    # Chart 3: Stock Status (donut)
    ax = axes[0, 2]
    counts = table["Stock_Status"].value_counts()
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", wedgeprops={"width": 0.4})
    ax.set_title("Stock Status", fontweight="bold")

    # Chart 4: Inventory Priority
    ax = axes[1, 0]
    order = ["Critical", "High", "Medium", "Low", "Unknown"]
    counts = table["Inventory_Priority"].value_counts().reindex(order, fill_value=0)
    bars = ax.bar(counts.index, counts.values, color="#f59e0b")
    ax.bar_label(bars)
    ax.set_title("Inventory Priority", fontweight="bold")
    ax.set_ylabel("Number of Products")

    # Chart 5: Critical Products - Reorder Cost
    ax = axes[1, 1]
    data = critical.sort_values("Reorder_Cost", ascending=False)
    ax.bar(data["Product_Name"], data["Reorder_Cost"].fillna(0), color="#ef4444")
    ax.set_title("Critical Products - Reorder Cost", fontweight="bold")
    ax.set_ylabel("Reorder Cost ($)")
    ax.tick_params(axis="x", rotation=45)

    # The last box is empty, so hide it
    axes[1, 2].axis("off")

    # Step 4: save the image
    plt.tight_layout(rect=[0, 0, 1, 0.82])
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "inventory_dashboard.png")
    fig.savefig(save_path, dpi=150)
    plt.close(fig)

    logger.info("Dashboard saved to %s", save_path)
    return save_path

