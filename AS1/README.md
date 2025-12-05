# AS1 - Producer–Consumer with Thread Synchronization (Python)

## Overview
This project implements the classic **producer–consumer pattern** to demonstrate
thread synchronization and inter-thread communication.

A **Producer** thread reads data from a source container and puts items into a
**bounded blocking queue**. A **Consumer** thread reads from the queue and
stores items into a destination container.

The implementation using Python’s `Lock` and `Condition`   
for shows a **wait/notify-style mechanism**


---

## Key Concepts Demonstrated
- **Thread synchronization** using locks and conditons
- **Concurrent programming** with multi threads
- **Bounded blocking queues** 
- **Wait/notify mechanism** (via `Condition.wait()` / `notify()`)
- **Thread-safe containers** for safe access
- **Sentinel pattern** for signaling completion
- **Timeout handle**  

---

## Design

### Components
- **`BlockingQueue`**
  - A bounded queue implemented with:
    - `threading.Lock` for mutual exclusion
    - two `threading.Condition` objects (`not_full`, `not_empty`)
  - `put()` blocks if the queue is full.
  - `get()` blocks if the queue is empty.
  - `qsize()`, `empty()`, `full()`  for thread-safe size

- **`SourceContainer`**
- Container stores source data
- Procide safe iteration
- Creates internal copy to avoid external mutation

- **`DestinationContainer`**
- Provides thread-safe access

- **`Producer`**
  - Reads items from `SourceContainer`.
  - Pushes items to the queue.
  - Sends a **unique sentinel** object to signal completion.
  - Tracks count

- **`Consumer`**
  - Reads items from the queue.
  - Writes items to `DestinationContainer`.
  - Stops when it receives the sentinel.
  - Tracks count

### Sentinel Choice
A dedicated sentinel object is used to avoid collisions with valid data values.

---

## Setup

From the project root:

```bash
cd AS1
python -m venv venv
source venv/bin/activate   # macOS/Linux
# .\venv\Scripts\activate  # Windows
```

## Excution
```
python main.py
```

## Test
```
python test_producer_consumer.py
```

## Test Cover
- TestBlockingQueue: Queue operations, blocking behavior, timeouts
- TestSourceContainer: Initialization, isolation, iteration
- TestDestinationContainer: Thread-safe operations
- TestProducerConsumer: Single producer-consumer scenarios
- TestStress: Large data transfers, minimal queues, rapid cycles
- TestSentinel: Sentinel uniqueness and identity checks

