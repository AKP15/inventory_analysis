import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch, Rectangle

from src.logger import get_logger

logger = get_logger(__name__)

# ---------- Settings ----------
CARD_W, CARD_H = 0.17, 0.10
KPI_X = [0.10, 0.30, 0.50, 0.70, 0.90]
KPI_Y = 0.88
ACCENTS = ["#6366f1", "#0ea5e9", "#10b981", "#f59e0b", "#ef4444"]

PRIORITY_ORDER = ["Critical", "High", "Medium", "Low", "Unknown"]
PRIORITY_COLORS = {
    "Critical": "#ef4444",
    "High": "#f59e0b",
    "Medium": "#0ea5e9",
    "Low": "#10b981",
    "Unknown": "#9ca3af",
}
STATUS_COLORS = {
    "Healthy": "#10b981",
    "Low Stock": "#ef4444",
    "Unknown": "#9ca3af",
}

REQUIRED_DF_COLUMNS = ["Stock_Quantity", "Unit_Cost", "Unit_Price"]
REQUIRED_TABLE_COLUMNS = [
    "Product_Name",
    "Inventory_Value",
    "Inventory_Turnover",
    "Stock_Status",
    "Inventory_Priority",
    "Reorder_Cost",
]


# ---------- Step 1: KPI numbers ----------
def calculate_kpis(df: pd.DataFrame, table: pd.DataFrame) -> dict:
    """Calculate the 5 KPI values. Returns {label: text}."""
    stock = df["Stock_Quantity"]

    inventory_value = (stock * df["Unit_Cost"]).sum()
    sales_value = (stock * df["Unit_Price"]).sum()
    gross_profit = sales_value - inventory_value

    critical = table[table["Inventory_Priority"] == "Critical"]
    critical_cost = critical["Reorder_Cost"].sum()

    return {
        "Total Inventory Value": f"${inventory_value:,.0f}",
        "Potential Sales Value": f"${sales_value:,.0f}",
        "Potential Gross Profit": f"${gross_profit:,.0f}",
        "Critical Products": f"{len(critical)}",
        "Critical Reorder Cost": f"${critical_cost:,.0f}",
    }


# ---------- Step 2: KPI cards ----------
def draw_kpi_cards(fig, kpis: dict) -> None:
    """Draw the 5 KPI cards on the top row of the figure."""
    for cx, accent, (label, value) in zip(KPI_X, ACCENTS, kpis.items()):
        x0 = cx - CARD_W / 2
        y0 = KPI_Y - CARD_H / 2

        # soft shadow
        fig.add_artist(FancyBboxPatch(
            (x0 + 0.002, y0 - 0.004), CARD_W, CARD_H,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            edgecolor="none", facecolor="#e5e7eb",
            transform=fig.transFigure, zorder=1))

        # white card
        fig.add_artist(FancyBboxPatch(
            (x0, y0), CARD_W, CARD_H,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            edgecolor="none", facecolor="white",
            transform=fig.transFigure, zorder=2))

        # colored strip on the left side of the card
        fig.add_artist(Rectangle(
            (x0 - 0.004, y0 + 0.012), 0.005, CARD_H - 0.024,
            edgecolor="none", facecolor=accent,
            transform=fig.transFigure, zorder=3))

        left = x0 + 0.012
        fig.text(left, KPI_Y + 0.020, label.upper(),
                 ha="left", va="center", color="#6b7280",
                 fontweight="bold", fontsize=11, zorder=4)
        fig.text(left, KPI_Y - 0.012, value,
                 ha="left", va="center", color="#111827",
                 fontweight="bold", fontsize=28, zorder=4)


# ---------- Step 3: charts ----------
def style_axis(ax, title: str, ylabel: str = "") -> None:
    """Common look for all bar charts."""
    ax.set_title(title, fontweight="bold", fontsize=13)
    ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.margins(y=0.12)  # leave room above bars for value labels


def draw_bar_chart(ax, labels, values, title, ylabel, colors, fmt) -> None:
    """Bar chart with value labels on top of each bar."""
    bars = ax.bar(labels, values, color=colors)
    style_axis(ax, title, ylabel)
    ax.tick_params(axis="x", rotation=45)
    for tick in ax.get_xticklabels():
        tick.set_ha("right")
    ax.bar_label(bars, labels=[fmt.format(v) for v in values],
                 padding=2, fontsize=7)


def draw_inventory_value(ax, table: pd.DataFrame) -> None:
    data = table.sort_values("Inventory_Value", ascending=False)
    draw_bar_chart(ax, data["Product_Name"], data["Inventory_Value"].fillna(0),
                   "Inventory Value by Product", "Inventory Value ($)",
                   "#6366f1", "${:,.0f}")


def draw_inventory_turnover(ax, table: pd.DataFrame) -> None:
    data = table.sort_values("Inventory_Turnover", ascending=False)
    draw_bar_chart(ax, data["Product_Name"], data["Inventory_Turnover"].fillna(0),
                   "Inventory Turnover by Product", "Turnover",
                   "#0ea5e9", "{:.2f}")


def draw_stock_status(ax, table: pd.DataFrame) -> None:
    counts = table["Stock_Status"].value_counts()
    colors = [STATUS_COLORS.get(status, "#9ca3af") for status in counts.index]

    ax.pie(counts.values, labels=counts.index, colors=colors,
           autopct="%1.1f%%", pctdistance=0.8, startangle=90,
           wedgeprops={"width": 0.4, "edgecolor": "white"})
    ax.text(0, 0, f"{counts.sum()}\nproducts", ha="center", va="center",
            fontweight="bold", fontsize=12)
    ax.set_title("Stock Status", fontweight="bold", fontsize=13)


def draw_inventory_priority(ax, table: pd.DataFrame) -> None:
    counts = table["Inventory_Priority"].value_counts()
    counts = counts.reindex(PRIORITY_ORDER, fill_value=0)
    colors = [PRIORITY_COLORS[p] for p in counts.index]

    bars = ax.bar(counts.index, counts.values, color=colors)
    style_axis(ax, "Inventory Priority", "Number of Products")
    ax.bar_label(bars, padding=2)


def draw_critical_reorder_cost(ax, table: pd.DataFrame) -> None:
    critical = table[table["Inventory_Priority"] == "Critical"]
    critical = critical.sort_values("Reorder_Cost", ascending=False)

    if critical.empty:
        ax.axis("off")
        ax.set_title("Critical Products - Reorder Cost", fontweight="bold", fontsize=13)
        ax.text(0.5, 0.5, "No critical products", ha="center", va="center",
                transform=ax.transAxes, color="#6b7280")
        return

    draw_bar_chart(ax, critical["Product_Name"], critical["Reorder_Cost"].fillna(0),
                   "Critical Products - Reorder Cost", "Reorder Cost ($)",
                   PRIORITY_COLORS["Critical"], "${:,.0f}")


# ---------- Main function ----------
def create_dashboard(
    df: pd.DataFrame,
    table: pd.DataFrame,
    save_dir: str = "dashbook",
    file_name: str = "inventory_dashboard.png",
    show: bool = False,
) -> str:
    """
    Build the inventory dashboard and save it as a PNG.

    df    : cleaned row-level data (used for the KPI cards)
    table : product table with Reorder_Cost, Movement_Status and Inventory_Priority
    Returns the path of the saved image.
    """
    logger.info("Dashboard started")

    missing_df = [c for c in REQUIRED_DF_COLUMNS if c not in df.columns]
    missing_table = [c for c in REQUIRED_TABLE_COLUMNS if c not in table.columns]
    if missing_df or missing_table:
        logger.error("Dashboard failed. Missing in df: %s | Missing in table: %s",
                     missing_df, missing_table)
        raise ValueError("Dashboard failed: missing columns")

    kpis = calculate_kpis(df, table)

    fig = plt.figure(figsize=(20, 12))
    fig.suptitle("Inventory Dashboard", fontsize=22, fontweight="bold", y=0.985)

    draw_kpi_cards(fig, kpis)

    # 6 columns: top row has 3 charts (2 columns each), bottom row has 2 charts (3 columns each)
    grid = fig.add_gridspec(2, 6, left=0.05, right=0.97, top=0.76, bottom=0.10,
                            hspace=0.8, wspace=1.0)

    draw_inventory_value(fig.add_subplot(grid[0, 0:2]), table)
    draw_inventory_turnover(fig.add_subplot(grid[0, 2:4]), table)
    draw_stock_status(fig.add_subplot(grid[0, 4:6]), table)
    draw_inventory_priority(fig.add_subplot(grid[1, 0:3]), table)
    draw_critical_reorder_cost(fig.add_subplot(grid[1, 3:6]), table)

    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, file_name)
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    logger.info("Dashboard saved to %s", save_path)

    if show:
        plt.show()
    plt.close(fig)

    return save_path
