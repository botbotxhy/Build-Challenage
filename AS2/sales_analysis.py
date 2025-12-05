import csv
from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from itertools import groupby
from typing import Iterable, List, Dict, Tuple, TextIO


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
        """
        Compute revenue for this record (quantity * unit_price).
        """
        return self.quantity * self.unit_price


def parse_date(s: str) -> datetime:
    """
    Parse dates of the form YYYY-MM-DD.
    """
    return datetime.strptime(s, "%Y-%m-%d")


def load_sales_records(file_obj: TextIO) -> List[SalesRecord]:
    """
    Load sales records from a CSV file-like object using DictReader.
    This demonstrates a 'stream' of rows mapped into SalesRecord objects.
    """
    reader = csv.DictReader(file_obj)

    # functional-style transformation from row dicts to SalesRecord
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


# ---------- Aggregation / Stream-style operations ----------

def total_revenue(records: Iterable[SalesRecord]) -> float:
    """
    Total revenue across all records.
    Uses reduce + lambda to demonstrate functional style.
    """
    return reduce(lambda acc, r: acc + r.revenue, records, 0.0)


def revenue_by_region(records: Iterable[SalesRecord]) -> Dict[str, float]:
    """
    Group by region and sum revenue, using reduce as a stream-style fold.
    """
    def step(acc: Dict[str, float], r: SalesRecord) -> Dict[str, float]:
        acc[r.region] = acc.get(r.region, 0.0) + r.revenue
        return acc

    return reduce(step, records, {})


def revenue_by_product(records: Iterable[SalesRecord]) -> Dict[str, float]:
    """
    Group by product and sum revenue.
    """
    def step(acc: Dict[str, float], r: SalesRecord) -> Dict[str, float]:
        acc[r.product] = acc.get(r.product, 0.0) + r.revenue
        return acc

    return reduce(step, records, {})


def units_sold_by_product(records: Iterable[SalesRecord]) -> Dict[str, int]:
    """
    Group by product and sum quantities sold.
    """
    def step(acc: Dict[str, int], r: SalesRecord) -> Dict[str, int]:
        acc[r.product] = acc.get(r.product, 0) + r.quantity
        return acc

    return reduce(step, records, {})


def top_n_products_by_revenue(
    records: Iterable[SalesRecord],
    n: int
) -> List[Tuple[str, float]]:
    """
    Return the top N products by total revenue, as (product, revenue) pairs.
    Uses sorted + lambda for a stream-like terminal operation.
    """
    revenue_map = revenue_by_product(records)
    return sorted(
        revenue_map.items(),
        key=lambda kv: kv[1],   # kv = (product, revenue)
        reverse=True
    )[:n]


def monthly_revenue(records: Iterable[SalesRecord]) -> Dict[str, float]:
    """
    Compute revenue grouped by month (YYYY-MM).
    Demonstrates grouping via itertools.groupby over a sorted stream.
    """
    def key_func(r: SalesRecord) -> str:
        return f"{r.date.year:04d}-{r.date.month:02d}"

    # Copy to a list so we can sort once, simulating a sorted stream
    rec_list = list(records)
    rec_list.sort(key=key_func)

    result: Dict[str, float] = {}
    for month, group in groupby(rec_list, key=key_func):
        # group is an iterator (stream) consumed by total_revenue
        result[month] = total_revenue(group)
    return result


# Optional: small demo if you *do* run this file directly
if __name__ == "__main__":
    # Example of how you'd wire it up in a real run:
    import io

    sample_csv = io.StringIO(
        "order_id,date,region,salesperson,product,quantity,unit_price\n"
        "1,2025-01-15,North,Alice,Widget,10,5.0\n"
        "2,2025-01-20,North,Bob,Gadget,5,12.0\n"
    )
    recs = load_sales_records(sample_csv)
    print("Total revenue:", total_revenue(recs))
