import unittest
from io import StringIO

from sales_analysis import (
    load_sales_records,
    total_revenue,
    revenue_by_region,
    revenue_by_product,
    units_sold_by_product,
    top_n_products_by_revenue,
    monthly_revenue,
)

CSV_DATA = """order_id,date,region,salesperson,product,quantity,unit_price
1,2025-01-15,North,Alice,Widget,10,5.0
2,2025-01-20,North,Bob,Gadget,5,12.0
3,2025-02-10,South,Alice,Widget,3,5.0
4,2025-02-11,South,Charlie,Thing,7,8.0
5,2025-02-12,East,Bob,Gadget,2,12.0
"""

EMPTY_CSV = "order_id,date,region,salesperson,product,quantity,unit_price\n"


class TestSalesAnalysis(unittest.TestCase):
    def setUp(self):
        self.records = load_sales_records(StringIO(CSV_DATA))

    def test_load_sales_records(self):
        self.assertEqual(len(self.records), 5)
        self.assertEqual(self.records[0].product, "Widget")

    def test_total_revenue(self):
        expected = 10*5.0 + 5*12.0 + 3*5.0 + 7*8.0 + 2*12.0
        self.assertAlmostEqual(total_revenue(self.records), expected)

    def test_revenue_by_region(self):
        rev = revenue_by_region(self.records)
        self.assertAlmostEqual(rev["North"], 10*5.0 + 5*12.0)
        self.assertAlmostEqual(rev["South"], 3*5.0 + 7*8.0)
        self.assertAlmostEqual(rev["East"], 2*12.0)

    def test_revenue_by_product(self):
        rev = revenue_by_product(self.records)
        self.assertAlmostEqual(rev["Widget"], 10*5.0 + 3*5.0)
        self.assertAlmostEqual(rev["Gadget"], 5*12.0 + 2*12.0)
        self.assertAlmostEqual(rev["Thing"], 7*8.0)

    def test_units_sold_by_product(self):
        units = units_sold_by_product(self.records)
        self.assertEqual(units["Widget"], 13)
        self.assertEqual(units["Gadget"], 7)
        self.assertEqual(units["Thing"], 7)

    def test_top_n_products_by_revenue_basic(self):
        top2 = top_n_products_by_revenue(self.records, 2)
        self.assertEqual(len(top2), 2)
        self.assertGreaterEqual(top2[0][1], top2[1][1])

    def test_top_n_products_by_revenue_n_zero(self):
        self.assertEqual(top_n_products_by_revenue(self.records, 0), [])

    def test_top_n_products_by_revenue_n_large(self):
        top = top_n_products_by_revenue(self.records, 999)
        # should not crash, should return all unique products
        self.assertTrue(len(top) <= 3)

    def test_monthly_revenue(self):
        mr = monthly_revenue(self.records)
        jan = 10*5.0 + 5*12.0
        feb = 3*5.0 + 7*8.0 + 2*12.0
        self.assertAlmostEqual(mr["2025-01"], jan)
        self.assertAlmostEqual(mr["2025-02"], feb)

    def test_empty_dataset(self):
        empty_records = load_sales_records(StringIO(EMPTY_CSV))
        self.assertEqual(total_revenue(empty_records), 0.0)
        self.assertEqual(revenue_by_region(empty_records), {})
        self.assertEqual(revenue_by_product(empty_records), {})
        self.assertEqual(units_sold_by_product(empty_records), {})
        self.assertEqual(top_n_products_by_revenue(empty_records, 3), [])
        self.assertEqual(monthly_revenue(empty_records), {})


if __name__ == "__main__":
    unittest.main()
