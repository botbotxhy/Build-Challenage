""" 
Unit test for the Implementation

Test:
- BlockingQueue 
- P-C coordination
- Thread Safety
- Timeout
- Stress Test
"""

import time
import unittest
import threading
from concurrent.futures import ThreadPoolExecutor

from producer_consumer import (
    BlockingQueue,
    SourceContainer,
    DestinationContainer,
    Producer,
    Consumer,
    SENTINEL,
)

# For Blocking
class TestBlockingQueue(unittest.TestCase):
    def test_put_get_single_item(self):
        q = BlockingQueue(maxsize=1)
        q.put(42)
        self.assertEqual(q.get(), 42)

    def test_invalid_maxsize(self):
        with self.assertRaises(ValueError):
            BlockingQueue(0)
            
    def test_invalid_maxsize_negative(self):
        with self.assertRaises(ValueError):
            BlockingQueue(-5)
            
    def test_qsize(self):
        """Test queue size reporting."""
        q = BlockingQueue(maxsize=5)
        self.assertEqual(q.qsize(), 0)
        q.put(1)
        self.assertEqual(q.qsize(), 1)
        q.put(2)
        self.assertEqual(q.qsize(), 2)
        q.get()
        self.assertEqual(q.qsize(), 1)
        
    def test_empty_and_full(self):
        q = BlockingQueue(maxsize=2)
        self.assertTrue(q.empty())
        self.assertFalse(q.full())
        
        q.put(1)
        self.assertFalse(q.empty())
        self.assertFalse(q.full())
        
        q.put(2)
        self.assertFalse(q.empty())
        self.assertTrue(q.full())

    def test_queue_blocks_when_full(self):
        q = BlockingQueue(maxsize=1)
        q.put("first")

        def delayed_get():
            time.sleep(0.2)
            q.get()

        t = threading.Thread(target=delayed_get)
        t.start()

        start = time.time()
        q.put("second")
        elapsed = time.time() - start

        t.join()
        self.assertGreaterEqual(elapsed, 0.19)
        
    def test_queue_blocks_when_empty(self):
        q = BlockingQueue(maxsize=1)

        def delayed_put():
            time.sleep(0.2)
            q.put("item")

        t = threading.Thread(target=delayed_put)
        t.start()

        start = time.time()
        item = q.get()
        elapsed = time.time() - start

        t.join()
        self.assertEqual(item, "item")
        self.assertGreaterEqual(elapsed, 0.15)
        
    
    def test_put_timeout(self):
        q = BlockingQueue(maxsize=1)
        q.put("first")
        
        with self.assertRaises(TimeoutError):
            q.put("second", timeout=0.1)
            
    def test_put_timeout(self):
        q = BlockingQueue(maxsize=1)
        q.put("first")
        
        with self.assertRaises(TimeoutError):
            q.put("second", timeout=0.1)

class TestSourceContainer(unittest.TestCase):
    """Tests for the SourceContainer class."""

    def test_initialization(self):
        """Test initializes"""
        data = [1, 2, 3]
        src = SourceContainer(data)
        self.assertEqual(list(src), data)

    def test_isolation_from_original(self):
        """Test that source container doesn't affect original list."""
        data = [1, 2, 3]
        src = SourceContainer(data)
        data.append(4)
        self.assertEqual(list(src), [1, 2, 3])

    def test_iteration(self):
        """Test iteration over source container."""
        data = ["a", "b", "c"]
        src = SourceContainer(data)
        result = [item for item in src]
        self.assertEqual(result, data)

class TestDestinationContainer(unittest.TestCase):
    """Tests for the DestinationContainer class."""

    def test_add_items(self):
        """Test adding items to destination."""
        dest = DestinationContainer()
        dest.add(1)
        dest.add(2)
        self.assertEqual(dest.items, [1, 2])

    def test_len(self):
        """Test length reporting."""
        dest = DestinationContainer()
        self.assertEqual(len(dest), 0)
        dest.add("item")
        self.assertEqual(len(dest), 1)
        
class TestProducerConsumer(unittest.TestCase):
    def test_single_producer_single_consumer_order_preserved(self):
        data = list(range(100))
        src = SourceContainer(data)
        dest = DestinationContainer()
        queue = BlockingQueue(maxsize=10)

        producer = Producer(src, queue)
        consumer = Consumer(dest, queue)

        producer.start()
        consumer.start()
        producer.join()
        consumer.join()

        self.assertEqual(dest.items, data)

    def test_empty_source(self):
        src = SourceContainer([])
        dest = DestinationContainer()
        queue = BlockingQueue(maxsize=2)

        producer = Producer(src, queue)
        consumer = Consumer(dest, queue)

        producer.start()
        consumer.start()
        producer.join()
        consumer.join()

        self.assertEqual(dest.items, [])
        
    def test_single_item(self):
        src = SourceContainer([42])
        dest = DestinationContainer()
        queue = BlockingQueue(maxsize=1)

        producer = Producer(src, queue)
        consumer = Consumer(dest, queue, propagate_sentinel=False)

        producer.start()
        consumer.start()
        producer.join()
        consumer.join()

        self.assertEqual(dest.items, [42])
        
    def test_items_produced_count(self):
        data = list(range(50))
        src = SourceContainer(data)
        dest = DestinationContainer()
        queue = BlockingQueue(maxsize=5)

        producer = Producer(src, queue)
        consumer = Consumer(dest, queue, propagate_sentinel=False)

        producer.start()
        consumer.start()
        producer.join()
        consumer.join()

        self.assertEqual(producer.items_produced, 50)
        self.assertEqual(consumer.items_consumed, 50)
        
    def test_none_as_valid_data(self):
        data = [None, 1, None, 2, None]
        src = SourceContainer(data)
        dest = DestinationContainer()
        queue = BlockingQueue(maxsize=3)

        producer = Producer(src, queue)
        consumer = Consumer(dest, queue, propagate_sentinel=False)

        producer.start()
        consumer.start()
        producer.join()
        consumer.join()

        self.assertEqual(dest.items, data)
        
    def test_custom_sentinel(self):
        custom_sentinel = "STOP"
        data = [1, 2, 3]
        src = SourceContainer(data)
        dest = DestinationContainer()
        queue = BlockingQueue(maxsize=2)

        producer = Producer(src, queue, sentinel=custom_sentinel)
        consumer = Consumer(dest, queue, sentinel=custom_sentinel, propagate_sentinel=False)

        producer.start()
        consumer.start()
        producer.join()
        consumer.join()

        self.assertEqual(dest.items, data)
        
class TestStress(unittest.TestCase):
    def test_large_data_transfer(self):
        data = list(range(10000))
        src = SourceContainer(data)
        dest = DestinationContainer()
        queue = BlockingQueue(maxsize=100)

        producer = Producer(src, queue)
        consumer = Consumer(dest, queue, propagate_sentinel=False)

        producer.start()
        consumer.start()
        producer.join()
        consumer.join()

        self.assertEqual(dest.items, data)
    
    def test_tiny_queue(self):
        data = list(range(1000))
        src = SourceContainer(data)
        dest = DestinationContainer()
        queue = BlockingQueue(maxsize=1)

        producer = Producer(src, queue)
        consumer = Consumer(dest, queue, propagate_sentinel=False)

        producer.start()
        consumer.start()
        producer.join()
        consumer.join()

        self.assertEqual(dest.items, data)
        
    def test_rapid_produce_consume(self):
        for _ in range(10):
            data = list(range(100))
            src = SourceContainer(data)
            dest = DestinationContainer()
            queue = BlockingQueue(maxsize=5)

            producer = Producer(src, queue)
            consumer = Consumer(dest, queue, propagate_sentinel=False)

            producer.start()
            consumer.start()
            producer.join()
            consumer.join()

            self.assertEqual(dest.items, data)

class TestSentinel(unittest.TestCase):
    def test_sentinel_is_unique(self):
        self.assertIsNot(SENTINEL, None)
        self.assertIsNot(SENTINEL, 0)
        self.assertIsNot(SENTINEL, "")
        self.assertIsNot(SENTINEL, [])

    def test_sentinel_identity_check(self):
        # Create an object that equals everything
        class EqualToAll:
            def __eq__(self, other):
                return True
        
        equal_obj = EqualToAll()
        self.assertTrue(equal_obj == SENTINEL)
        self.assertIsNot(equal_obj, SENTINEL)

if __name__ == "__main__":
    unittest.main()
