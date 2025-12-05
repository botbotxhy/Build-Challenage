from producer_consumer import (
    BlockingQueue,
    SourceContainer,
    DestinationContainer,
    Producer,
    Consumer,
)

def main():
    # create source data
    source_data = list(range(10))
    src = SourceContainer(source_data)
    dest = DestinationContainer()

    # create a queue with bound and its capacity of 3, 
    # this one shows the blocking
    queue = BlockingQueue(maxsize=3)
    
    # create producer and consumer threads
    producer = Producer(src, queue, name="MainProducer")
    consumer = Consumer(dest, queue, name="MainConsumer", propagate_sentinel=False)

    # start threads
    producer.start()
    consumer.start()

    # wait for complete
    producer.join()
    consumer.join()

    #show the output
    print("=" * 60)
    print("Implement producer-consumer pattern with thread synchronization")
    print("=" * 60)
    print(f"Queue capacity:      {queue._maxsize}")
    print(f"Source items:        {source_data}")
    print(f"Destination items:   {dest.items}")
    print(f"Items produced:      {producer.items_produced}")
    print(f"Items consumed:      {consumer.items_consumed}")
    print(f"Transfer correct:    {dest.items == source_data}")
    print("=" * 60)


if __name__ == "__main__":
    main()
