from pathlib import Path
from sales_analysis import (
    load_sales_records,
    total_revenue,
    revenue_by_region,
    revenue_by_product,
    units_sold_by_product,
    revenue_by_salesperson,
    top_n_products_by_revenue,
    top_n_salespersons,
    monthly_revenue,
    filter_by_region,
    filter_high_value_sales,
    top_products_in_region,
    salesperson_performance_in_region,
    average_order_value,
    average_order_value_by_region,
    sales_count_by_region,
    sort_records_by_revenue,
)

def print_section(title: str):
    print(f"\n{'='*50}")
    print(f" {title}")
    print('='*50)

def main():
    # Load data (sample_sales.csv generate by AI)
    csv_path = Path(__file__).with_name("sample_sales.csv")
    
    with csv_path.open("r", encoding="utf-8") as f:
        records = load_sales_records(f)

    print("Sales Data Analysis")

    # Aggregations 
    print_section("Aggregations")
    
    print(f"Total Revenue: ${total_revenue(records):,.2f}")
    print(f"Average Order Value: ${average_order_value(records):,.2f}")
    print(f"Number of Transactions: {len(records)}")

    # Revenue Breakdowns
    print_section("Revenue by Region")
    for region, rev in sorted(revenue_by_region(records).items()):
        print(f"  {region}: ${rev:,.2f}")

    print_section("Revenue by Product")
    for product, rev in sorted(revenue_by_product(records).items(), key=lambda x: x[1], reverse=True):
        print(f"  {product}: ${rev:,.2f}")

    print_section("Units Sold by Product")
    for product, units in sorted(units_sold_by_product(records).items(), key=lambda x: x[1], reverse=True):
        print(f"  {product}: {units} units")

    # Rankings
    print_section("Top 3 Products by Revenue")
    for rank, (product, rev) in enumerate(top_n_products_by_revenue(records, 3), start=1):
        print(f"  {rank}. {product}: ${rev:,.2f}")

    print_section("Top 3 Salespersons by Revenue")
    for rank, (name, rev) in enumerate(top_n_salespersons(records, 3), start=1):
        print(f"  {rank}. {name}: ${rev:,.2f}")

    # Time-based Analysis
    print_section("Monthly Revenue")
    for month, rev in sorted(monthly_revenue(records).items()):
        print(f"  {month}: ${rev:,.2f}")

    # Filter Examples 
    print_section("Filter Examples")
    
    north_sales = filter_by_region(records, "North")
    print(f"Sales in North region: {len(north_sales)} transactions, ${total_revenue(north_sales):,.2f} revenue")
    
    high_value = filter_high_value_sales(records, 75.0)
    print(f"High-value sales (>$75): {len(high_value)} transactions")

    # Pipeline Operations
    print_section("Pipeline: Top Products in Each Region")
    for region in ["North", "South", "East", "West"]:
        top2 = top_products_in_region(records, region, 2)
        products_str = ", ".join(f"{p} (${r:,.2f})" for p, r in top2)
        print(f"  {region}: {products_str}")

    print_section("Average Order Value by Region")
    for region, avg in sorted(average_order_value_by_region(records).items()):
        print(f"  {region}: ${avg:,.2f}")

    print_section("Transaction Count by Region")
    for region, count in sorted(sales_count_by_region(records).items()):
        print(f"  {region}: {count} transactions")

    # Top Individual Sales
    print_section("Top 5 Individual Sales by Revenue")
    top_sales = sort_records_by_revenue(records, descending=True)[:5]
    for sale in top_sales:
        print(f"  Order {sale.order_id}: {sale.product} - {sale.quantity} x ${sale.unit_price:.2f} = ${sale.revenue:.2f} ({sale.salesperson}, {sale.region})")


if __name__ == "__main__":
    main()
