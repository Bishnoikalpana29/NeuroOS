#ifndef SYNCHRONIZATION_H
#define SYNCHRONIZATION_H

#include <mutex>
#include <condition_variable>
#include <queue>
#include <thread>
#include <iostream>
#include <stdexcept>

class SynchronizationDemo
{
private:
    // Shared data protected by a mutex.
    int sharedCounter;

    // Mutex protects access to sharedCounter.
    std::mutex counterMutex;

    // Bounded buffer for the producer-consumer problem.
    std::queue<int> buffer;

    // Maximum number of items allowed in the buffer.
    const int bufferSize;

    // Protects the buffer.
    std::mutex bufferMutex;

    // Coordinates producer and consumer threads.
    std::condition_variable bufferNotFull;
    std::condition_variable bufferNotEmpty;

public:
    explicit SynchronizationDemo(int size = 5);

    // Demonstrate mutual exclusion.
    void incrementCounter(int iterations);

    // Demonstrate the producer-consumer problem.
    void producer(int itemCount);
    void consumer(int itemCount);

    // Display the final shared counter.
    void displayCounter();
};

#endif