import pandas as pd 
from src.logger import get_logger
from src.validator import validate
from src.cleaner import clean
from src.kpi import create_new_column
from src.analyzer import product_summary, stock_status, stock_status_summary,product_table,add_priority,add_reorder_quantity,add_reorder_cost
from src.dashbook import create_dashboard

logger = get_logger(__name__)
path="data/data.csv"
if __name__ == "__main__":
    df = pd.read_csv(path)
    pd.to_datetime(df['Order_Date'])
    
    results = validate(df)
    df = clean(df)
    validate(df)
    create_new_column(df)
    product_summary = product_summary(df)
    df = stock_status(df)
    stock_status_summary=stock_status_summary(df)
    table = product_table(df)
    table = add_priority(table)
    table = add_reorder_quantity(table)
    table = add_reorder_cost(table)
    create_dashboard(df, table)
    print(df.columns)
    print(table.columns)
    


