# AS1 - Producer–Consumer with Thread Synchronization (Python)

## Overview
This project implements the producer-consumer problem for threading/concurrency.

Two threads running at the same time:
- Produces data
- Consumes data

These two threads share a queue in between. 
The producer grabs items from a source list and drops them into a shared queue.  
The consumer picks items out of that queue and stores them elsewhere. 

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

- This project uses only the Python 3 standard library.

---

## Excution
```
python main.py
```

## Test
```
python test_producer_consumer.py
```

## Test Cover
- TestBlockingQueue
- TestSourceContainer
- TestDestinationContainer
- TestProducerConsumer
- TestStress
- TestSentinel

## Example Output
============================================================
Implement producer-consumer pattern with thread synchronization
============================================================
Queue capacity:      3
Source items:        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Destination items:   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Items produced:      10
Items consumed:      10
Transfer correct:    True
============================================================