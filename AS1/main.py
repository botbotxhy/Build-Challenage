from producer_consumer import (
    BlockingQueue,
    SourceContainer,
    DestinationContainer,
    Producer,
    Consumer,
)

def main():
    src = SourceContainer(list(range(10)))
    dest = DestinationContainer()
    queue = BlockingQueue(maxsize=3)

    producer = Producer(src, queue)
    consumer = Consumer(dest, queue)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    print("Implement producer-consumer pattern with thread synchronization")
    print("Source items:     ", src.items)
    print("Destination items:", dest.items)
    print("Transfer correct:", dest.items == src.items)

if __name__ == "__main__":
    main()
