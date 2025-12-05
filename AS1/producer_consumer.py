# producer_consumer.py
import threading
from typing import Any, List

# Unique sentinel object (cannot collide with real data)
SENTINEL = object()


class BlockingQueue:
    """
    Simple bounded blocking queue implemented with Lock + Condition.
    Demonstrates wait()/notify() coordination.
    """
    def __init__(self, maxsize: int):
        if maxsize <= 0:
            raise ValueError("maxsize must be positive")
        self._maxsize = maxsize
        self._items: List[Any] = []
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)

    def put(self, item: Any) -> None:
        with self._not_full:
            while len(self._items) >= self._maxsize:
                self._not_full.wait()
            self._items.append(item)
            self._not_empty.notify()

    def get(self) -> Any:
        with self._not_empty:
            while not self._items:
                self._not_empty.wait()
            item = self._items.pop(0)
            self._not_full.notify()
            return item

    def qsize(self) -> int:
        with self._lock:
            return len(self._items)


class SourceContainer:
    def __init__(self, items: List[Any]):
        self.items = list(items)


class DestinationContainer:
    def __init__(self):
        self.items: List[Any] = []

    def add(self, item: Any) -> None:
        self.items.append(item)


class Producer(threading.Thread):
    def __init__(self, src: SourceContainer, queue: BlockingQueue, sentinel: Any = SENTINEL):
        super().__init__()
        self.src = src
        self.queue = queue
        self.sentinel = sentinel

    def run(self) -> None:
        for item in self.src.items:
            self.queue.put(item)
        self.queue.put(self.sentinel)


class Consumer(threading.Thread):
    def __init__(self, dest: DestinationContainer, queue: BlockingQueue, sentinel: Any = SENTINEL):
        super().__init__()
        self.dest = dest
        self.queue = queue
        self.sentinel = sentinel

    def run(self) -> None:
        while True:
            item = self.queue.get()
            if item is self.sentinel:
                self.queue.put(self.sentinel)
                break
            self.dest.add(item)
