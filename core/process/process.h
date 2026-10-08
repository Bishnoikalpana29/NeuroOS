#ifndef PROCESS_H
#define PROCESS_H

#include <string>

struct Process {
    int pid;
    std::string name;

    int arrivalTime;
    int burstTime;
    int priority;

    int remainingTime;
    int waitingTime;
    int turnaroundTime;
    int completionTime;

    Process(int id, std::string processName,
            int arrival, int burst, int prio)
    {
        pid = id;
        name = processName;

        arrivalTime = arrival;
        burstTime = burst;
        priority = prio;

        remainingTime = burst;
        waitingTime = 0;
        turnaroundTime = 0;
        completionTime = 0;
    }
};

#endif