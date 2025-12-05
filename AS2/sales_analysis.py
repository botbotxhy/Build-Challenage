""" 
Sales Analysis

Analyzing sales data. 
Shows reduce, filter, map, groupby, and lambda expressions
"""
import csv
from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from itertools import groupby
from operator import attrgetter
from typing import List, Dict, Tuple, TextIO, Iterator, Callable


@dataclass(frozen=True)
class SalesRecord:
    """
    Immutable record representing one row of the sales CSV.
    """
    order_id: str
    date: datetime
    region: str
    salesperson: str
    product: str
    quantity: int
    unit_price: float

    @property
    def revenue(self) -> float:
        """revenus = quantity * unit_price"""
        return self.quantity * self.unit_price


def parse_date(s: str) -> datetime:
    """Parse dates of the form YYYY-MM-DD."""
    return datetime.strptime(s, "%Y-%m-%d")


def load_sales_records(file_obj: TextIO) -> List[SalesRecord]:
    """Load sales records from a CSV file"""
    reader = csv.DictReader(file_obj)

    def row_to_record(row: Dict[str, str]) -> SalesRecord:
        return SalesRecord(
            order_id=row["order_id"],
            date=parse_date(row["date"]),
            region=row["region"],
            salesperson=row["salesperson"],
            product=row["product"],
            quantity=int(row["quantity"]),
            unit_price=float(row["unit_price"]),
        )

    return list(map(row_to_record, reader))


#  Aggregation Function

def total_revenue(records: List[SalesRecord]) -> float:
    """ Calculate the revenue through sum of all records"""
    return reduce(lambda acc, r: acc + r.revenue, records, 0.0)


def revenue_by_region(records: List[SalesRecord]) -> Dict[str, float]:
    """Group by region and sum revenue"""
    def accumulate(acc: Dict[str, float], record: SalesRecord) -> Dict[str, float]:
        acc[record.region] = acc.get(record.region, 0.0) + record.revenue
        return acc

    return reduce(accumulate, records, {})


def revenue_by_product(records: List[SalesRecord]) -> Dict[str, float]:
    """Group by product and sum revenue."""
    def accumulate(acc: Dict[str, float], record: SalesRecord) -> Dict[str, float]:
        acc[record.product] = acc.get(record.product, 0.0) + record.revenue
        return acc

    return reduce(accumulate, records, {})


def units_sold_by_product(records: List[SalesRecord]) -> Dict[str, int]:
    """Group by product and sum quantities sold."""
    def accumulate(acc: Dict[str, int], record: SalesRecord) -> Dict[str, int]:
        acc[record.product] = acc.get(record.product, 0) + record.quantity
        return acc

    return reduce(accumulate, records, {})

def revenue_by_salesperson(records: List[SalesRecord]) -> Dict[str, float]:
    """Group records by salesperson and sum their revenue."""
    def accumulate(acc: Dict[str, float], record: SalesRecord) -> Dict[str, float]:
        acc[record.salesperson] = acc.get(record.salesperson, 0.0) + record.revenue
        return acc

    return reduce(accumulate, records, {})

# Filter Function

def filter_by_region(records: List[SalesRecord], region: str) -> List[SalesRecord]:
    """Keep only records from the specified region."""
    return list(filter(lambda r: r.region == region, records))


def filter_by_product(records: List[SalesRecord], product: str) -> List[SalesRecord]:
    """Keep only records for the specified product."""
    return list(filter(lambda r: r.product == product, records))


def filter_by_salesperson(records: List[SalesRecord], name: str) -> List[SalesRecord]:
    """Keep only records for the specified salesperson."""
    return list(filter(lambda r: r.salesperson == name, records))


def filter_high_value_sales(records: List[SalesRecord], threshold: float) -> List[SalesRecord]:
    """Keep only records where revenue exceeds the threshold."""
    return list(filter(lambda r: r.revenue > threshold, records))


def filter_by_date_range(
    records: List[SalesRecord],
    start: datetime,
    end: datetime
) -> List[SalesRecord]:
    """Keep records within a date range (inclusive)"""
    return list(filter(lambda r: start <= r.date <= end, records))

# Sorting and Ranking

def top_n_products_by_revenue(
    records: List[SalesRecord],
    n: int
) -> List[Tuple[str, float]]:
    """Return the top N products by total revenue, as (product, revenue) pairs"""
    revenue_map = revenue_by_product(records)
    ranked = sorted(revenue_map.items(), key=lambda item: item[1], reverse=True)
    return ranked[:n]


def top_n_salespersons(records: List[SalesRecord], n: int) -> List[Tuple[str, float]]:
    """Return the top N salespersons ranked by total revenue."""
    revenue_map = revenue_by_salesperson(records)
    ranked = sorted(revenue_map.items(), key=lambda item: item[1], reverse=True)
    return ranked[:n]

def sort_records_by_revenue(records: List[SalesRecord], descending: bool = True) -> List[SalesRecord]:
    """Sort records by their individual revenue."""
    return sorted(records, key=attrgetter('revenue'), reverse=descending)


def sort_records_by_date(records: List[SalesRecord]) -> List[SalesRecord]:
    """Sort records chronologically using attrgetter."""
    return sorted(records, key=attrgetter('date'))

# Grouping

def monthly_revenue(records: List[SalesRecord]) -> Dict[str, float]:
    """Compute revenue grouped by month"""
    def key_func(r: SalesRecord) -> str:
        return f"{r.date.year:04d}-{r.date.month:02d}"

    def month_key(record: SalesRecord) -> str:
        return f"{record.date.year:04d}-{record.date.month:02d}"

    sorted_records = sorted(records, key=month_key)
    
    result: Dict[str, float] = {}
    for month, group in groupby(sorted_records, key=month_key):
        result[month] = total_revenue(list(group))
    
    return result

def sales_count_by_region(records: List[SalesRecord]) -> Dict[str, int]:
    """Count how many sales transactions occurred in each region."""
    def accumulate(acc: Dict[str, int], record: SalesRecord) -> Dict[str, int]:
        acc[record.region] = acc.get(record.region, 0) + 1
        return acc

    return reduce(accumulate, records, {})

# Pipeline

def top_products_in_region(
    records: List[SalesRecord],
    region: str,
    n: int
) -> List[Tuple[str, float]]:
    """Find top N products by revenue within a specific region."""
    regional_records = filter_by_region(records, region)
    return top_n_products_by_revenue(regional_records, n)


def salesperson_performance_in_region(
    records: List[SalesRecord],
    region: str
) -> List[Tuple[str, float]]:
    """ Rank salespersons by revenue within a specific region."""
    regional_records = filter_by_region(records, region)
    revenue_map = revenue_by_salesperson(regional_records)
    return sorted(revenue_map.items(), key=lambda item: item[1], reverse=True)


def average_order_value(records: List[SalesRecord]) -> float:
    """Calculate the average revenue per order."""
    if not records:
        return 0.0
    return total_revenue(records) / len(records)


def average_order_value_by_region(records: List[SalesRecord]) -> Dict[str, float]:
    """Calculate average order value for each region."""
    regions = set(map(lambda r: r.region, records))
    return {
        region: average_order_value(filter_by_region(records, region))
        for region in regions
    }

if __name__ == "__main__":
    import io

    sample_csv = io.StringIO(
        "order_id,date,region,salesperson,product,quantity,unit_price\n"
        "1,2025-01-15,North,Alice,Widget,10,5.0\n"
        "2,2025-01-20,North,Bob,Gadget,5,12.0\n"
    )
    
    recs = load_sales_records(sample_csv)
    print("Loaded records:", len(recs))
    print("Total revenue:", total_revenue(recs))
    print("Revenue by region:", revenue_by_region(recs))
    print("High value sales (>50):", len(filter_high_value_sales(recs, 50)))
