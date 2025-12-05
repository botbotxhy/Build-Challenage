# AS1 - Producer–Consumer with Thread Synchronization (Python)

## Overview
This project implements the classic **producer–consumer pattern** to demonstrate
safe thread synchronization and inter-thread communication.

A **Producer** thread reads data from a source container and places items into a
shared **bounded blocking queue**. A **Consumer** thread reads from the queue and
stores items into a destination container.

The implementation explicitly demonstrates a **wait/notify-style mechanism**
using Python’s `Lock` and `Condition`, mirroring the behavior of Java-style
`wait()` / `notify()` synchronization.

---

## Key Concepts Demonstrated
- **Thread synchronization**
- **Concurrent programming**
- **Bounded blocking queues**
- **Wait/notify mechanism** (via `Condition.wait()` / `notify()`)

---

## Design

### Components
- **`BlockingQueue`**
  - A bounded queue implemented with:
    - `threading.Lock`
    - two `threading.Condition` objects (`not_full`, `not_empty`)
  - `put()` blocks when the queue is full.
  - `get()` blocks when the queue is empty.

- **`Producer`**
  - Reads items from `SourceContainer`.
  - Pushes items to the queue.
  - Sends a **unique sentinel** object to signal completion.

- **`Consumer`**
  - Reads items from the queue.
  - Writes items to `DestinationContainer`.
  - Stops when it receives the sentinel.

### Sentinel Choice
A dedicated sentinel object is used to avoid collisions with valid data values.
This improves correctness over using a common value like `None`.

---

## Setup

From the project root:

```bash
cd AS1
python -m venv venv
source venv/bin/activate   # macOS/Linux
# .\venv\Scripts\activate  # Windows
