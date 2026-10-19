📦 Inventory Analysis with Python

📌 Project Overview

This project analyzes inventory data to identify stock risks, fast- and slow-moving products, potential overstock, and replenishment priorities.

The goal is to simulate a real-world inventory analyst task using Python and provide actionable recommendations that could help a business improve inventory management and reduce stockout risk.

---

🎯 Business Objectives

This analysis aims to answer:

- How much inventory value does the business currently hold?
- What is the potential sales value of the inventory?
- Which products are fast-moving?
- Which products are slow-moving?
- Which products are at risk of stockout?
- Which products should be reordered immediately?
- How much would replenishment cost?
- Which products may have potential overstock?
- Where is the business's inventory investment concentrated?

---

🗂️ Dataset

The dataset contains 50 inventory records and 10 columns.

Column| Description
"Product_ID"| Unique product identifier
"Product_Name"| Product name
"Category"| Product category
"Supplier"| Product supplier
"Stock_Quantity"| Current recorded stock quantity
"Reorder_Level"| Stock level at which replenishment is needed
"Unit_Cost"| Cost to purchase one unit
"Unit_Price"| Selling price per unit
"Units_Sold"| Number of units sold
"Order_Date"| Date of the inventory/sales record

---

🧹 Data Cleaning

The dataset contained several intentional data-quality issues.

Issues identified

- Missing "Stock_Quantity"
- Negative "Unit_Cost"
- Inconsistent category capitalization
- "Order_Date" stored as an object
- Duplicate checks performed
- Product ID uniqueness checked

Cleaning decisions

- Corrected the negative "Unit_Cost" for Monitor 24 inch from "-110" to "110".
- Standardized category names such as "electronics" → "Electronics".
- Converted "Order_Date" to datetime.
- Kept the missing Webcam stock value as unknown rather than arbitrarily imputing it.
- Confirmed there were no duplicate rows or duplicate Product IDs.

---

📊 Key Inventory Metrics

Inventory Value

Inventory Value = Stock Quantity × Unit Cost

Potential Sales Value

Potential Sales Value = Stock Quantity × Unit Price

Potential Gross Profit

Potential Gross Profit = Potential Sales Value − Inventory Value

Simplified Inventory Turnover

Inventory Turnover ≈ Units Sold ÷ Stock Quantity

«Note: This is a simplified operational turnover metric for this project. It is not the formal accounting inventory turnover ratio because beginning/average inventory was not available.»

---

📈 Key Results

KPI| Result
Total Inventory Value| $19,054
Potential Sales Value| $39,550
Potential Gross Profit| $20,496
Critical Products| 6
Critical Reorder Cost| $4,335

---

🚨 Critical Inventory Products

Products were classified as Critical when they were both:

«Fast Moving + Low Stock»

The analysis identified six critical products:

Product| Turnover| Reorder Quantity| Reorder Cost
Webcam| 5.73| 30| $840
Monitor 24 inch| 3.78| 12| $1,320
Printer| 3.20| 9| $1,080
Headphones| 2.83| 15| $450
Keyboard| 1.85| 6| $120
Office Chair| 1.74| 7| $525
Total| | 79| $4,335

🔴 Recommendation

These six products should be prioritized for replenishment.

The Webcam requires the largest quantity increase at 30 units and has the highest inventory turnover at 5.73, making it a particularly important stockout-risk product.

---

⚠️ Potential Overstock

Products classified as:

«Healthy Stock + Slow Moving»

were investigated as potential overstock candidates.

The most notable example is:

Wireless Mouse

- Inventory Value: $2,062.50
- Inventory Turnover: 0.47
- Stock Status: Healthy
- Movement: Slow

This does not prove that the product is overstocked. However, the relatively high inventory value combined with slow movement suggests that the product should be investigated before additional inventory is purchased.

---

📊 Dashboard

The planned dashboard focuses on business decision-making rather than displaying every possible metric.

KPI Cards

- Total Inventory Value
- Potential Sales Value
- Potential Gross Profit
- Critical Products
- Critical Reorder Cost

Charts

1. Inventory Value by Product
   - Shows where inventory investment is concentrated.
2. Inventory Turnover by Product
   - Identifies fast- and slow-moving products.
3. Stock Status
   - Shows the overall inventory health.
4. Inventory Priority
   - Highlights products requiring attention.
5. Critical Products — Reorder Cost
   - Shows the financial cost of replenishing critical inventory.

---

💡 Business Insights

1. Stockout Risk

Six products are classified as critical because they combine high movement with low stock.

2. Replenishment Investment

The estimated replenishment cost for the six critical products is:

$4,335

3. Fastest-Moving Product

Webcam has the highest simplified inventory turnover:

5.73

4. Potential Overstock

Wireless Mouse has the highest inventory value among the slow-moving products:

$2,062.50

This product should be monitored before placing additional orders.

5. Inventory Profit Potential

The current inventory has:

- Potential Sales Value: $39,550
- Inventory Cost: $19,054
- Potential Gross Profit: $20,496

---

🛠️ Tools & Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

---

🔍 Analysis Workflow

Raw Data
   ↓
Data Inspection
   ↓
Data Cleaning
   ↓
Data Validation
   ↓
Inventory Metrics
   ↓
Product-Level Analysis
   ↓
Inventory Turnover
   ↓
Stock Status
   ↓
Movement Classification
   ↓
Inventory Priority
   ↓
Reorder Analysis
   ↓
Financial Impact
   ↓
Business Recommendations
   ↓
Dashboard

---

⚠️ Project Limitations

This project uses a simplified inventory dataset, so some calculations are approximations.

Stock Quantity

Stock quantity appears as inventory observations over time. Summing stock across historical records does not represent a true current inventory balance.

For a production inventory system, the latest stock record per product should generally be used for current-stock decisions.

Inventory Turnover

The turnover calculation uses:

Units Sold ÷ Stock Quantity

A formal inventory turnover calculation would normally use Cost of Goods Sold ÷ Average Inventory.

Reorder Quantity

The reorder calculation is simplified as:

Reorder Quantity = Reorder Level − Current Stock

A production system would ideally consider:

- Lead time
- Average daily/weekly demand
- Safety stock
- Supplier reliability
- Seasonality
- Purchase order quantities

---

🚀 Future Improvements

Potential improvements include:

- Use the latest inventory record for current stock.
- Calculate demand velocity by week/month.
- Add safety stock calculations.
- Calculate reorder points using supplier lead time.
- Add ABC inventory classification.
- Analyze inventory by category and supplier.
- Add monthly inventory trends.
- Build an interactive dashboard using Power BI or Streamlit.
- Add automated low-stock alerts.

---

👨‍💻 Project Purpose

This project was created as part of my Data Analyst internship practice portfolio to develop practical skills in:

- Data cleaning
- Exploratory data analysis
- Business metrics
- Inventory analysis
- Data-driven decision making
- Business recommendations
- Data visualization
- Python/Pandas

---

📌 Final Takeaway

The analysis demonstrates how raw inventory data can be transformed into actionable business insights.

The main recommendation is to replenish the six critical fast-moving products, while monitoring slow-moving products such as Wireless Mouse for potential excess inventory.

The analysis estimates $4,335 in replenishment costs for the critical products while identifying $19,054 of inventory value currently tied up in stock.
