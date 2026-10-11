#include "synchronization.h"

SynchronizationDemo::SynchronizationDemo(int size)
    : sharedCounter(0),
      bufferSize(size)
{
    if (size <= 0)
    {
        throw std::invalid_argument(
            "Buffer size must be greater than zero."
        );
    }
}

void SynchronizationDemo::incrementCounter(int iterations)
{
    for (int i = 0; i < iterations; i++)
    {
        // Only one thread can modify sharedCounter at a time.
        std::lock_guard<std::mutex> lock(counterMutex);

        sharedCounter++;
    }
}

void SynchronizationDemo::displayCounter()
{
    std::lock_guard<std::mutex> lock(counterMutex);

    std::cout << "Final shared counter: "
              << sharedCounter << std::endl;
}

void SynchronizationDemo::producer(int itemCount)
{
    for (int i = 1; i <= itemCount; i++)
    {
        std::unique_lock<std::mutex> lock(bufferMutex);

        // Wait until the buffer has space.
        bufferNotFull.wait(lock, [this]()
        {
            return buffer.size() < static_cast<std::size_t>(bufferSize);
        });

        // Add an item to the buffer.
        buffer.push(i);

        std::cout << "Producer produced: " << i << std::endl;

        // Release the lock before notifying the consumer.
        lock.unlock();

        bufferNotEmpty.notify_one();
    }
}

void SynchronizationDemo::consumer(int itemCount)
{
    for (int i = 0; i < itemCount; i++)
    {
        std::unique_lock<std::mutex> lock(bufferMutex);

        // Wait until an item is available.
        bufferNotEmpty.wait(lock, [this]()
        {
            return !buffer.empty();
        });

        // Remove an item from the buffer.
        int item = buffer.front();
        buffer.pop();

        std::cout << "Consumer consumed: "
                  << item << std::endl;

        // Release the lock before notifying the producer.
        lock.unlock();

        bufferNotFull.notify_one();
    }
}