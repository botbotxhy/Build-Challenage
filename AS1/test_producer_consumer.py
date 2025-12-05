import time
import unittest
import threading

from producer_consumer import (
    BlockingQueue,
    SourceContainer,
    DestinationContainer,
    Producer,
    Consumer,
    SENTINEL,
)

class TestBlockingQueue(unittest.TestCase):
    def test_put_get_single_item(self):
        q = BlockingQueue(maxsize=1)
        q.put(42)
        self.assertEqual(q.get(), 42)

    def test_invalid_maxsize(self):
        with self.assertRaises(ValueError):
            BlockingQueue(0)

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

if __name__ == "__main__":
    unittest.main()
