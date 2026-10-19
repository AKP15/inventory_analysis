import pandas as pd
from src.logger import get_logger

logger = get_logger(__name__)

EXPECTED_COLUMNS = ['Product_ID', 'Product_Name', 'Category', 'Supplier', 
                    'Stock_Quantity','Reorder_Level', 'Unit_Cost', 
                    'Unit_Price', 'Units_Sold', 'Order_Date']

def check_columns(df: pd.DataFrame) -> bool:
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    extra = [c for c in df.columns if c not in EXPECTED_COLUMNS]
    if extra:
        logger.warning("Unexpected columns found: %s", extra)
    if missing:
        logger.error("Missing columns: %s", missing)
        return False
    logger.info("Column check passed: all %d columns present", len(EXPECTED_COLUMNS))
    return True

def _report(column: str, bad: int) -> None:
    if bad:
        logger.warning(f"{column} check failed: {bad}  invalid rows")
    else:
        logger.info(f"{column} check passed")

def check_product_id(df: pd.DataFrame) -> int:
    ids = df["Product_ID"]
    bad = (ids.isna() | (ids.astype(str).str.strip() == "") | ids.duplicated()).sum()
    _report("Product_ID", bad)
    return int(bad)

def check_product_name(df: pd.DataFrame) -> int:
    names = df["Product_Name"]
    bad = (names.isna() | (names.astype(str).str.strip() == "")).sum()
    _report("Product_Name", bad)
    return int(bad)

def check_category(df: pd.DataFrame) -> int:
    values = df["Category"]
    bad = (values.nunique() - values.str.strip().str.lower().nunique())
    _report("Category", bad)
    return int(bad)

def check_supplier(df: pd.DataFrame) -> int:
    values = df["Supplier"]
    bad = (values.isna() | (values.astype(str).str.strip() == "")).sum()
    _report("Supplier", bad)
    return int(bad)

def check_stock_quantity(df: pd.DataFrame) -> int:
    stock = pd.to_numeric(df["Stock_Quantity"], errors="coerce")
    bad = (stock.isna() | (stock < 0)).sum()
    _report("Stock_Quantity", bad)
    return int(bad)

def check_reorder_level(df: pd.DataFrame) -> int:
    level = pd.to_numeric(df["Reorder_Level"], errors="coerce")
    bad = (level.isna() | (level < 0)).sum()
    _report("Reorder_Level", bad)
    return int(bad)

def check_unit_cost(df: pd.DataFrame) -> int:
    cost = pd.to_numeric(df["Unit_Cost"], errors="coerce")
    bad = (cost.isna() | (cost <= 0)).sum()
    _report("Unit_Cost", bad)
    return int(bad)

def check_unit_price(df: pd.DataFrame) -> int:
    price = pd.to_numeric(df["Unit_Price"], errors="coerce")
    bad = (price.isna() | (price <= 0)).sum()
    _report("Unit_Price", bad)
    return int(bad)

def check_price_vs_cost(df: pd.DataFrame) -> int:
    cost = pd.to_numeric(df["Unit_Cost"], errors="coerce")
    price = pd.to_numeric(df["Unit_Price"], errors="coerce")
    bad = (price < cost).sum()
    _report("Price vs Cost", bad)
    return int(bad)

def check_units_sold(df: pd.DataFrame) -> int:
    sold = pd.to_numeric(df["Units_Sold"], errors="coerce")
    bad = (sold.isna() | (sold < 0)).sum()
    _report("Units_Sold", bad)
    return int(bad)

def check_order_date(df: pd.DataFrame) -> int:
    dates = pd.to_datetime(df["Order_Date"], errors="coerce")
    bad = dates.isna().sum()
    _report("Order_Date", bad)
    return int(bad)

def validate(df: pd.DataFrame) -> dict:
    results = {
            "Check_Column" : check_columns(df),
            "Product_ID": check_product_id(df),
            "Product_Name": check_product_name(df),
            "Category": check_category(df),
            "Supplier": check_supplier(df),
            "Stock_Quantity": check_stock_quantity(df),
            "Reorder_Level": check_reorder_level(df),
            "Unit_Cost": check_unit_cost(df),
            "Unit_Price": check_unit_price(df),
            "Price_vs_Cost": check_price_vs_cost(df),
            "Units_Sold": check_units_sold(df),
            "Order_Date": check_order_date(df),
            }
    logger.info(f"Validation finished: {sum(results.values())}  invalid rows in total")
    return results
