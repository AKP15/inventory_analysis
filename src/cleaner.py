import pandas as pd
from src.logger import get_logger
logger = get_logger(__name__)

def standardize_category(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    count = (df["Category"] == "electronics").sum()
    df["Category"] = df["Category"].replace("electronics", "Electronics")
    logger.info("Category: fixed %d values", count)
    return df


def fix_negative_unit_cost(df: pd.DataFrame) -> pd.DataFrame:       
    df = df.copy()
    cost = pd.to_numeric(df["Unit_Cost"], errors="coerce")
    negative = cost < 0
    count = int(negative.sum())
    if count:
        df.loc[negative, "Unit_Cost"] = cost[negative].abs()
        logger.info("Unit_Cost: fixed %d negative values", count)
    else:
        logger.info("Unit_Cost: no negative values found")
    return df

def fix_order_date(df:pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Order_Date"]=pd.to_datetime(df["Order_Date"], errors="coerce")
    return df

def clean(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Cleaning started")
    df = standardize_category(df)
    df = fix_negative_unit_cost(df)
    df = fix_order_date(df)
    logger.info("Cleaning finished")
    return df

