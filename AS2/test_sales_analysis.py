import unittest
from io import StringIO
from datetime import datetime

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
    filter_by_product,
    filter_by_salesperson,
    filter_high_value_sales,
    filter_by_date_range,
    top_products_in_region,
    salesperson_performance_in_region,
    average_order_value,
    average_order_value_by_region,
    sales_count_by_region,
    sort_records_by_revenue,
    sort_records_by_date,
    SalesRecord,
)

CSV_DATA = """order_id,date,region,salesperson,product,quantity,unit_price
1,2025-01-15,North,Alice,Widget,10,5.0
2,2025-01-20,North,Bob,Gadget,5,12.0
3,2025-02-10,South,Alice,Widget,3,5.0
4,2025-02-11,South,Charlie,Thing,7,8.0
5,2025-02-12,East,Bob,Gadget,2,12.0
"""

EMPTY_CSV = "order_id,date,region,salesperson,product,quantity,unit_price\n"

SINGLE_RECORD_CSV = """order_id,date,region,salesperson,product,quantity,unit_price
1,2025-03-01,West,Dana,Gizmo,4,25.0
"""

class TestSalesAnalysis(unittest.TestCase):
    def test_load_correct_count(self):
        records = load_sales_records(StringIO(CSV_DATA))
        self.assertEqual(len(records), 5)

    def test_load_empty_csv(self):
        records = load_sales_records(StringIO(EMPTY_CSV))
        self.assertEqual(len(records), 0)

    def test_load_single_record(self):
        records = load_sales_records(StringIO(SINGLE_RECORD_CSV))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].product, "Gizmo")
        self.assertEqual(records[0].quantity, 4)
    
    def test_record_fields_parsed_correctly(self):
        records = load_sales_records(StringIO(CSV_DATA))
        first = records[0]
        self.assertEqual(first.order_id, "1")
        self.assertEqual(first.region, "North")
        self.assertEqual(first.salesperson, "Alice")
        self.assertEqual(first.product, "Widget")
        self.assertEqual(first.quantity, 10)
        self.assertEqual(first.unit_price, 5.0)

    def test_date_parsing(self):
        records = load_sales_records(StringIO(CSV_DATA))
        self.assertEqual(records[0].date, datetime(2025, 1, 15))

    def test_revenue_property(self):
        records = load_sales_records(StringIO(CSV_DATA))
        # First record: 10 * 5.0 = 50.0
        self.assertAlmostEqual(records[0].revenue, 50.0)

# Test Aggregation
class TestBasicAggregations(unittest.TestCase):            
    def setUp(self):
        self.records = load_sales_records(StringIO(CSV_DATA))

    def test_load_sales_records(self):
        self.assertEqual(len(self.records), 5)
        self.assertEqual(self.records[0].product, "Widget")

    def test_total_revenue(self):
        # 10*5 + 5*12 + 3*5 + 7*8 + 2*12 = 50 + 60 + 15 + 56 + 24 = 205
        expected = 10*5.0 + 5*12.0 + 3*5.0 + 7*8.0 + 2*12.0
        self.assertAlmostEqual(total_revenue(self.records), expected)

    def test_revenue_by_region(self):
        rev = revenue_by_region(self.records)
        self.assertAlmostEqual(rev["North"], 10*5.0 + 5*12.0) # expected: 110
        self.assertAlmostEqual(rev["South"], 3*5.0 + 7*8.0) # expected: 71
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
        
    def test_revenue_by_salesperson(self):
        rev = revenue_by_salesperson(self.records)
        # Sample test
        # Alice: 50 + 15 = 65
        # Bob: 60 + 24 = 84
        # Charlie: 56
        self.assertAlmostEqual(rev["Alice"], 65.0)
        self.assertAlmostEqual(rev["Bob"], 84.0)
        self.assertAlmostEqual(rev["Charlie"], 56.0)
    
    def test_sales_count_by_region(self):
        counts = sales_count_by_region(self.records)
        self.assertEqual(counts["North"], 2)
        self.assertEqual(counts["South"], 2)
        self.assertEqual(counts["East"], 1)
        
# Test Ranking
class TestRankings(unittest.TestCase):
    def setUp(self):
        self.records = load_sales_records(StringIO(CSV_DATA))
        
    def test_top_n_products_order(self):
        top2 = top_n_products_by_revenue(self.records, 2)
        self.assertEqual(len(top2), 2)
        # Gadget (84) should be first, and then Widget (65)
        self.assertEqual(top2[0][0], "Gadget")
        self.assertEqual(top2[1][0], "Widget")
    
    def test_top_n_products_zero(self):
        result = top_n_products_by_revenue(self.records, 0)
        self.assertEqual(result, [])
        
    def test_top_n_products_exceeds_count(self):
        # Only 3 unique products, asking for 10
        result = top_n_products_by_revenue(self.records, 10)
        self.assertEqual(len(result), 3)
        
    def test_top_n_salespersons(self):
        top2 = top_n_salespersons(self.records, 2)
        # Bob: 84, Alice: 65, Charlie: 56
        self.assertEqual(top2[0][0], "Bob")
        self.assertEqual(top2[1][0], "Alice")
        
    def test_sort_by_revenue_ascending(self):
        sorted_recs = sort_records_by_revenue(self.records, descending=False)
        # Lowest should be first
        revenues = [r.revenue for r in sorted_recs]
        self.assertEqual(revenues, sorted(revenues))
        
    def test_sort_by_revenue_descending(self):
        sorted_recs = sort_records_by_revenue(self.records, descending=True)
        # Highest revenue should be first
        revenues = [r.revenue for r in sorted_recs]
        self.assertEqual(revenues, sorted(revenues, reverse=True))

# Test Filter
class TestFilters(unittest.TestCase):  
    def setUp(self):
        self.records = load_sales_records(StringIO(CSV_DATA))
        
    def test_filter_by_region(self):
        north = filter_by_region(self.records, "North")
        self.assertEqual(len(north), 2)
        self.assertTrue(all(r.region == "North" for r in north))
    
    def test_filter_by_region_empty_result(self):
        result = filter_by_region(self.records, "West")
        self.assertEqual(len(result), 0)

    def test_filter_by_product(self):
        widgets = filter_by_product(self.records, "Widget")
        self.assertEqual(len(widgets), 2)
        self.assertTrue(all(r.product == "Widget" for r in widgets))

    def test_filter_by_salesperson(self):
        alice = filter_by_salesperson(self.records, "Alice")
        self.assertEqual(len(alice), 2)
        self.assertTrue(all(r.salesperson == "Alice" for r in alice))
        
    def test_filter_high_value_sales(self):
        high = filter_high_value_sales(self.records, 50.0)
        self.assertEqual(len(high), 2)  # expect: 60 and 56

    def test_filter_high_value_sales_none_match(self):
        result = filter_high_value_sales(self.records, 1000.0)
        self.assertEqual(len(result), 0)

    def test_filter_by_date_range(self):
        start = datetime(2025, 2, 1)
        end = datetime(2025, 2, 28)
        feb_records = filter_by_date_range(self.records, start, end)
        self.assertEqual(len(feb_records), 3)
 
# Test Pipeline
class TestPipelineOperations(unittest.TestCase): 
    def setUp(self):
        self.records = load_sales_records(StringIO(CSV_DATA))
    
    def test_top_products_in_region(self):
        top = top_products_in_region(self.records, "North", 2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0][0], "Gadget")
        
    def test_top_products_in_empty_region(self):
        result = top_products_in_region(self.records, "West", 5)
        self.assertEqual(result, [])
        
    def test_salesperson_performance_in_region(self):
        # North: Alice (50), Bob (60)
        perf = salesperson_performance_in_region(self.records, "North")
        self.assertEqual(perf[0][0], "Bob")  # Bob has 60, Alice has 50
    
    def test_average_order_value(self):
        # Total: 205, Count: 5 -> Avg: 41
        avg = average_order_value(self.records)
        self.assertAlmostEqual(avg, 41.0)
    
    def test_average_order_value_empty(self):
        empty = load_sales_records(StringIO(EMPTY_CSV))
        self.assertEqual(average_order_value(empty), 0.0)
    
    def test_average_order_value_by_region(self):
        avgs = average_order_value_by_region(self.records)
        # North: 110/2 = 55
        # South: 71/2 = 35.5
        # East: 24/1 = 24
        self.assertAlmostEqual(avgs["North"], 55.0)
        self.assertAlmostEqual(avgs["South"], 35.5)
        self.assertAlmostEqual(avgs["East"], 24.0)

#Test Monthly
class TestMonthlyRevenue(unittest.TestCase): 
    def setUp(self):
        self.records = load_sales_records(StringIO(CSV_DATA))
    
    def test_monthly_revenue_grouping(self):
        monthly = monthly_revenue(self.records)
        # Jan: 50 + 60 = 110
        # Feb: 15 + 56 + 24 = 95
        self.assertAlmostEqual(monthly["2025-01"], 110.0)
        self.assertAlmostEqual(monthly["2025-02"], 95.0)

    def test_monthly_revenue_empty(self):
        empty = load_sales_records(StringIO(EMPTY_CSV))
        self.assertEqual(monthly_revenue(empty), {})
        
# Test Edgecase                                 
class TestEdgeCases(unittest.TestCase):
    def test_single_record_aggregations(self):
        records = load_sales_records(StringIO(SINGLE_RECORD_CSV))
        # 4 * 25 = 100
        self.assertAlmostEqual(total_revenue(records), 100.0)
        self.assertEqual(revenue_by_region(records), {"West": 100.0})
        self.assertEqual(units_sold_by_product(records), {"Gizmo": 4})

    def test_all_same_region(self):
        csv = "order_id,date,region,salesperson,product,quantity,unit_price\n1,2025-01-01,North,Alice,A,1,10.0\n2,2025-01-02,North,Bob,B,2,20.0\n3,2025-01-03,North,Charlie,C,3,30.0\n"
        records = load_sales_records(StringIO(csv))
        rev = revenue_by_region(records)
        self.assertEqual(len(rev), 1)
        self.assertIn("North", rev)

    def test_all_same_product(self):
        csv = "order_id,date,region,salesperson,product,quantity,unit_price\n1,2025-01-01,North,Alice,Widget,1,10.0\n2,2025-01-02,South,Bob,Widget,2,10.0\n3,2025-01-03,East,Charlie,Widget,3,10.0\n"
        records = load_sales_records(StringIO(csv))
        rev = revenue_by_product(records)
        self.assertEqual(len(rev), 1)
        self.assertAlmostEqual(rev["Widget"], 60.0)


if __name__ == "__main__":
    unittest.main()
