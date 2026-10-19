import pandas as pd
from src.logger import get_logger
logger = get_logger(__name__)

def product_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby("Product_Name")[[
        "Stock_Quantity",
        "Units_Sold",
        "Inventory_Value",
        "Potential_Sales_Value",
        "Potential_Gross_Profit",
        ]].sum()
    summary = summary.reset_index()
    summary["Inventory_Turnover"] = summary["Units_Sold"] / summary["Stock_Quantity"] 
    logger.info("Product summary created: %d products", len(summary))
    return summary

def classify(df: pd.DataFrame) -> None :
    Reorder_Level = pd.to_numeric(df['Reorder_Level'], errors = "coerce")
    Stock_Quantity = pd.to_numeric(df['Stock_Quantity'], errors = "coerce")
    if Stock_Quantity < Reorder_Level:
        return  "Low Stock" 
    elif Stock_Quantity >= Reorder_Level:
        return "Healthy"
    else:
        return "Unknown"

def stock_status(df: pd.DataFrame) -> pd.DataFrame:
    df['Stock_Status'] = df.apply(classify, axis=1)
    return df

def stock_status_summary(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["Stock_Status"].value_counts()
    counts = counts.reindex(["Low Stock", "Healthy", "Unknown"], fill_value=0)
    percentages = (counts / len(df) * 100).round(2)
    summary = pd.DataFrame({"Count": counts, "Percentage": percentages})
    logger.info("Stock status summary created")
    return summary

def product_table(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Inventory_Value"] = df["Stock_Quantity"] * df["Unit_Cost"]
    table = df.groupby("Product_Name").agg(
            Total_Stock=("Stock_Quantity", lambda x: x.sum(min_count=1)),
            Total_Units_Sold=("Units_Sold", "sum"),
            Inventory_Value=("Inventory_Value", "sum"),
            Total_Reorder_Level=("Reorder_Level", "sum"),
            Unit_Cost=("Unit_Cost", "mean"),
            ).reset_index()

    table["Inventory_Turnover"] = table["Total_Units_Sold"] / table["Total_Stock"]
    table["Inventory_Turnover"] = table["Inventory_Turnover"].replace(float("inf"), float("nan"))
    table["Inventory_Turnover"] = table["Inventory_Turnover"].round(2)


    table["Stock_Status"] = "Healthy"
    low = table["Total_Stock"] < table["Total_Reorder_Level"]
    table.loc[low, "Stock_Status"] = "Low Stock"
    missing = table["Total_Stock"].isna()
    table.loc[missing, "Stock_Status"] = "Unknown"

    table["Inventory_Value"] = table["Inventory_Value"].round(2)
    table = table.sort_values(by='Inventory_Turnover',ascending = False)
    logger.info("Product table created: %d products", len(table))
    return table

def add_priority(table: pd.DataFrame) -> pd.DataFrame:
    table = table.copy()
    median_turnover = table["Inventory_Turnover"].median()
    logger.info("Median Inventory_Turnover: %.2f", median_turnover)
    table["Movement_Status"] = "Slow Moving"
    table.loc[table["Inventory_Turnover"] >= median_turnover, "Movement_Status"] = "Fast Moving"
    table.loc[table["Inventory_Turnover"].isna(), "Movement_Status"] = "Unknown"
    low = table["Stock_Status"] == "Low Stock"
    healthy = table["Stock_Status"] == "Healthy"
    fast = table["Movement_Status"] == "Fast Moving"
    slow = table["Movement_Status"] == "Slow Moving"

    table["Inventory_Priority"] = "Unknown"
    table.loc[low & fast, "Inventory_Priority"] = "Critical"
    table.loc[low & slow, "Inventory_Priority"] = "Monitor"
    table.loc[healthy & fast, "Inventory_Priority"] = "Watch"
    table.loc[healthy & slow, "Inventory_Priority"] = "Normal"
    order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4, "Unknown": 5}
    table["Priority_Order"] = table["Inventory_Priority"].map(order)
    table = table.sort_values(
            ["Priority_Order", "Inventory_Turnover"], ascending=[True, False]
                        )
    table = table.drop(columns="Priority_Order").reset_index(drop=True)
    return table

def add_reorder_quantity(table: pd.DataFrame) -> pd.DataFrame:
    table = table.copy()
    table["Reorder_Quantity"] = table["Total_Reorder_Level"] - table["Total_Stock"]
    # If stock is above the reorder level, nothing to order
    table["Reorder_Quantity"] = table["Reorder_Quantity"].clip(lower=0)
    logger.info("Reorder_Quantity added")
    return table

def add_reorder_cost(table: pd.DataFrame) -> pd.DataFrame:
    table = table.copy()
    table["Reorder_Cost"] = table["Reorder_Quantity"] * table["Unit_Cost"]
    table["Reorder_Cost"] = table["Reorder_Cost"].round(2)
    logger.info("Reorder_Cost added")
    return table






            

