#include "synchronization.h"

#include <vector>

int main()
{
    std::cout << "====================================\n";
    std::cout << " NeuroOS Process Synchronization\n";
    std::cout << "====================================\n";

    SynchronizationDemo demo(5);

    // --------------------------------
    // Test 1: Mutual Exclusion
    // --------------------------------

    std::cout << "\nTest 1: Mutual Exclusion\n";

    const int threadCount = 4;
    const int iterations = 100000;

    std::vector<std::thread> threads;

    for (int i = 0; i < threadCount; i++)
    {
        threads.push_back(
            std::thread(
                &SynchronizationDemo::incrementCounter,
                &demo,
                iterations
            )
        );
    }

    for (std::size_t i = 0; i < threads.size(); i++)
    {
        threads[i].join();
    }

    demo.displayCounter();

    // --------------------------------
    // Test 2: Producer-Consumer
    // --------------------------------

    std::cout << "\nTest 2: Producer-Consumer\n";

    std::thread producerThread(
        &SynchronizationDemo::producer,
        &demo,
        10
    );

    std::thread consumerThread(
        &SynchronizationDemo::consumer,
        &demo,
        10
    );

    producerThread.join();
    consumerThread.join();

    std::cout << "\nSynchronization tests finished.\n";

    return 0;
}