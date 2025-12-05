# AS2/main.py
from pathlib import Path
from sales_analysis import (
    load_sales_records,
    total_revenue,
    revenue_by_region,
    revenue_by_product,
    units_sold_by_product,
    top_n_products_by_revenue,
    monthly_revenue,
)

def main():
    csv_path = Path(__file__).with_name("sample_sales.csv")

    with csv_path.open("r", encoding="utf-8") as f:
        records = load_sales_records(f)

    print("=== AS2 Sales Analysis ===")
    print(f"Loaded records: {len(records)}")
    print()

    print("1) Total Revenue")
    print(total_revenue(records))
    print()

    print("2) Revenue by Region")
    print(revenue_by_region(records))
    print()

    print("3) Revenue by Product")
    print(revenue_by_product(records))
    print()

    print("4) Units Sold by Product")
    print(units_sold_by_product(records))
    print()

    print("5) Top 3 Products by Revenue")
    print(top_n_products_by_revenue(records, 3))
    print()

    print("6) Monthly Revenue")
    print(monthly_revenue(records))
    print()

if __name__ == "__main__":
    main()
