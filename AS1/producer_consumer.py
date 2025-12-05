"""
Producer-consumer Pattern Implementation

This Module implements the classic producer-consumer pattern which showing the thread 
synchronization and commuication using python
"""

import threading
from collections import deque
from typing import Any, List, Optional

# Unique sentinel object (cannot collide with real data)
SENTINEL = object()

class BlockingQueue:
    """
    A bounded blocking queue implemented with Lock + Condition.
    Demonstrates wait()/notify() coordination.
    """
    def __init__(self, maxsize: int):
        # init
        if maxsize <= 0:
            raise ValueError("maxsize must be positive")
        self._maxsize = maxsize
        self._items: deque = deque()
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)

    def put(self, item: Any, timeout: Optional[float] = None) -> None:
        """Put an item into queue, blocking if the queue if full"""
        with self._not_full:
            while len(self._items) >= self._maxsize:
                if not self._not_full.wait(timeout):
                    raise TimeoutError("Queue put timed out")
            self._items.append(item)
            self._not_empty.notify()

    def get(self, timeout:Optional[float] = None) -> Any:
        """ Remove and return the item from queue, and same, blocking if empty"""
        with self._not_empty:
            while not self._items:
                if not self._not_empty.wait(timeout):
                    raise TimeoutError("Queue get timed out")
            item = self._items.popleft()  
            self._not_full.notify()
            return item

    def qsize(self) -> int:
        """ Return the number of items"""
        with self._lock:
            return len(self._items)
        
    def empty(self) -> bool:
        """ Return True if the queue is empty"""
        with self._lock:
            return len(self._items) == 0
        
    def full(self) -> bool:
        """Return True if the queue is full"""
        with self._lock:
            return len(self._items) >= self._maxsize


class SourceContainer:
    def __init__(self, items: List[Any]):
        self._lock = threading.Lock()
        self.items = list(items)
        
    def __iter__(self):
        with self._lock:
            return iter(list(self.items))

class DestinationContainer:
    """
    Container to store processed items for consumer
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._items: List[Any] = []

    def add(self, item: Any) -> None:
        """
        Add an item to container
        """
        with self._lock:
            self._items.append(item)

    @property
    def items(self) -> List[Any]:
        with self._lock:
            return list(self._items)

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)


class Producer(threading.Thread):
    def __init__(self, src: SourceContainer, queue: BlockingQueue, sentinel: Any = SENTINEL, name: Optional[str] = None):
        """
        A producer thread that reads items from a source and puts them into a queue.
        """
        super().__init__(name=name or "Producer")
        self.src = src
        self.queue = queue
        self.sentinel = sentinel
        self.items_produced = 0

    def run(self) -> None:
        try:
            for item in self.src:
                self.queue.put(item)
                self.items_produced += 1
        finally:
            self.queue.put(self.sentinel)

class Consumer(threading.Thread):
    def __init__(self, dest: DestinationContainer, queue: BlockingQueue, sentinel: Any = SENTINEL, name: Optional[str] = None, propagate_sentinel: bool = True):
        super().__init__(name=name or "Consumer")
        self.dest = dest
        self.queue = queue
        self.sentinel = sentinel
        self.propagate_sentinel = propagate_sentinel
        self.items_consumed = 0

    def run(self) -> None:
        while True:
            item = self.queue.get()
            if item is self.sentinel:
                if self.propagate_sentinel:
                    # Re-queue sentinel for other consumers in multi-consumer setup
                    self.queue.put(self.sentinel)
                break
            self.dest.add(item)
            self.items_consumed += 1
