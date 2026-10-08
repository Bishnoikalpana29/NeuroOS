#ifndef SCHEDULER_H
#define SCHEDULER_H

#include <string>
#include <vector>

struct Process
{
    int pid;
    std::string name;
    int arrivalTime;
    int burstTime;
    int priority;
    int memory;
    int io;
    std::string state;
};

struct ScheduleEntry
{
    int pid;
    int startTime;
    int endTime;
};

struct ProcessResult
{
    int pid;
    int completionTime;
    int turnaroundTime;
    int waitingTime;
    int responseTime;
};

struct ScheduleResult
{
    std::string algorithm;
    std::vector<ScheduleEntry> ganttChart;
    std::vector<ProcessResult> results;
    double averageTurnaroundTime;
    double averageWaitingTime;
    double averageResponseTime;
};

ScheduleResult fcfs(std::vector<Process> processes);

ScheduleResult sjf(std::vector<Process> processes);

ScheduleResult roundRobin(
    std::vector<Process> processes,
    int quantum
);

ScheduleResult priorityScheduling(
    std::vector<Process> processes
);

void printSchedule(const ScheduleResult& result);

#endif