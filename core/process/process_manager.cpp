#include <iostream>
#include <vector>
#include "process.h"

using namespace std;

void displayProcesses(const vector<Process>& processes)
{
    cout << "\n========== PROCESS TABLE ==========\n";

    cout << "PID\tName\tArrival\tBurst\tPriority\n";
    cout << "----------------------------------\n";

    for (const Process& p : processes)
    {
        cout << p.pid << "\t"
             << p.name << "\t"
             << p.arrivalTime << "\t"
             << p.burstTime << "\t"
             << p.priority << "\n";
    }

    cout << "==================================\n";
}

int main()
{
    vector<Process> processes;

    processes.emplace_back(1, "P1", 0, 8, 2);
    processes.emplace_back(2, "P2", 1, 4, 1);
    processes.emplace_back(3, "P3", 2, 6, 3);
    processes.emplace_back(4, "P4", 3, 5, 2);

    displayProcesses(processes);

    return 0;
}