import pandas as pd
from src.logger import get_logger
logger = get_logger(__name__)

def create_new(df:pd.DataFrame) -> pd.DataFrame:
    stock_quantity = pd.to_numeric(df['Stock_Quantity'], errors="coerce")
    unit_cost = pd.to_numeric(df['Unit_Cost'], errors = "coerce")
    unit_price = pd.to_numeric(df['Unit_Price'], errors = "coerce")
    df['Inventory_Value'] = stock_quantity * unit_cost
    df['Potential_Sales_Value'] = stock_quantity * unit_price
    df['Potential_Gross_Profit'] = df['Potential_Sales_Value'] - df['Inventory_Value']
    return df

def caculate_kpis(df:pd.DataFrame) -> dict:
    inv_val=pd.to_numeric(df['Inventory_Value'], errors = "coerce")
    psv=pd.to_numeric(df['Potential_Sales_Value'], errors = "coerce")
    pgv=pd.to_numeric(df['Potential_Gross_Profit'], errors = "coerce")
    total_inventory_value = inv_val.sum()
    total_potential_sales_value = psv.sum()
    total_potential_gross_profit = pgv.sum()
    kpis = {
            "total_inventory_value": total_inventory_value,
            "total_potential_sales_value" : total_potential_sales_value,
            "total_potential_gross_profit": total_potential_gross_profit
        }
    for name, value in kpis.items():
        logger.info(f"KPI | {name} = {value}")
    return kpis

def create_new_column(df:pd.DataFrame) -> pd.DataFrame:
    df = create_new(df)
    df = caculate_kpis(df)
    return df

