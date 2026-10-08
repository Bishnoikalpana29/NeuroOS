#include "scheduler.h"

#include <iostream>
#include <vector>

int main()
{
    std::vector<Process> processes =
    {
        {1, "P1", 0, 8, 2, 100, 20, "READY"},
        {2, "P2", 1, 4, 1, 120, 10, "READY"},
        {3, "P3", 2, 2, 3, 80, 15, "READY"},
        {4, "P4", 3, 1, 2, 90, 5, "READY"}
    };

    std::cout << "========================================\n";
    std::cout << "        NeuroOS CPU Scheduler\n";
    std::cout << "========================================\n";

    std::cout << "\nProcesses:\n";

    for (const auto& process : processes)
    {
        std::cout
            << "P"
            << process.pid
            << " | Arrival: "
            << process.arrivalTime
            << " | Burst: "
            << process.burstTime
            << " | Priority: "
            << process.priority
            << "\n";
    }

    ScheduleResult fcfsResult =
        fcfs(processes);

    printSchedule(fcfsResult);

    ScheduleResult sjfResult =
        sjf(processes);

    printSchedule(sjfResult);

    ScheduleResult priorityResult =
        priorityScheduling(processes);

    printSchedule(priorityResult);

    ScheduleResult rrResult =
        roundRobin(processes, 2);

    printSchedule(rrResult);

    return 0;
}