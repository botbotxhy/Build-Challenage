# AS2 - Sales Data Analysis (Functional / Stream-Style Python)

## Overview
This project demonstrates functional programming and stream-like data processing
in Python by performing aggregation and grouping operations on sales data stored
in CSV format.

The application loads sales records, computes revenue, and answers analytical
queries such as total revenue, revenue by region, revenue by product, units sold,
top-N products, and monthly revenue.

## Dataset
A synthetic dataset `sample_sales.csv` is included.

### Columns
- order_id
- date (YYYY-MM-DD)
- region
- salesperson
- product
- quantity (int)
- unit_price (float)

### Assumptions
- Revenue per record = quantity * unit_price
- Dates are valid and formatted correctly
- Dataset has no missing required columns

## Setup
From the project root:

```bash
cd AS2
python -m venv venv
source venv/bin/activate   # macOS/Linux
# .\venv\Scripts\activate  # Windows
python -m unittest test_sales_analysis.py 
```

## Run Analysis
```bash
python main.py
```

## Output
=== AS2 Sales Analysis ===
Loaded records: 60

1) Total Revenue
3600.349999999999

2) Revenue by Region
{'North': 1059.0, 'West': 844.6000000000001, 'South': 1006.25, 'East': 690.5}

3) Revenue by Product
{'Widget': 763.2, 'Gadget': 722.0999999999999, 'Thing': 546.85, 'Doohickey': 353.5, 'Gizmo': 618.25, 'Accessory': 596.45}

4) Units Sold by Product
{'Widget': 153, 'Gadget': 58, 'Thing': 66, 'Doohickey': 17, 'Gizmo': 40, 'Accessory': 184}

5) Top 3 Products by Revenue
[('Widget', 763.2), ('Gadget', 722.0999999999999), ('Gizmo', 618.25)]

6) Monthly Revenue
{'2025-01': 1126.5, '2025-02': 1246.1000000000001, '2025-03': 1227.7499999999998}

