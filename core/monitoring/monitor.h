#ifndef NEUROOS_MONITOR_H
#define NEUROOS_MONITOR_H

#include <string>

struct SystemMetrics {
    std::string timestamp;
    double cpuUtilizationPercent;
    double memoryUtilizationPercent;
    unsigned long long totalMemoryMB;
    unsigned long long usedMemoryMB;
    unsigned long long availableMemoryMB;
    unsigned long totalProcesses;
};

#endif