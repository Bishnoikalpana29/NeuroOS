#include "monitor.h"

#ifndef _WIN32_WINNT
#define _WIN32_WINNT 0x0600
#endif

#include <windows.h>
#include <tlhelp32.h>

extern "C" WINBASEAPI BOOL WINAPI GetSystemTimes(
    LPFILETIME lpIdleTime,
    LPFILETIME lpKernelTime,
    LPFILETIME lpUserTime
);

#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

namespace {

std::string currentTimestamp() {
    std::time_t now = std::time(NULL);
    std::tm* local = std::localtime(&now);

    if (local == NULL) {
        return "unknown";
    }

    char buffer[32];
    std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", local);
    return buffer;
}

unsigned long countProcesses() {
    unsigned long count = 0;

    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        return 0;
    }

    PROCESSENTRY32 entry;
    entry.dwSize = sizeof(entry);

    if (Process32First(snapshot, &entry)) {
        do {
            ++count;
        } while (Process32Next(snapshot, &entry));
    }

    CloseHandle(snapshot);
    return count;
}

bool collectMetrics(SystemMetrics& metrics,
                    unsigned long long& previousIdle,
                    unsigned long long& previousKernel,
                    unsigned long long& previousUser,
                    bool& hasPreviousCpuSample) {
    FILETIME idleTime, kernelTime, userTime;

    if (!GetSystemTimes(&idleTime, &kernelTime, &userTime)) {
        std::cerr << "Error: Could not read Windows CPU times.\n";
        return false;
    }

    ULONGLONG idle = (static_cast<ULONGLONG>(idleTime.dwHighDateTime) << 32)
                     | idleTime.dwLowDateTime;
    ULONGLONG kernel = (static_cast<ULONGLONG>(kernelTime.dwHighDateTime) << 32)
                       | kernelTime.dwLowDateTime;
    ULONGLONG user = (static_cast<ULONGLONG>(userTime.dwHighDateTime) << 32)
                     | userTime.dwLowDateTime;

    metrics.cpuUtilizationPercent = 0.0;

    if (hasPreviousCpuSample) {
        unsigned long long idleDelta = idle - previousIdle;
        unsigned long long kernelDelta = kernel - previousKernel;
        unsigned long long userDelta = user - previousUser;
        unsigned long long totalDelta = kernelDelta + userDelta;

        if (totalDelta > 0 && idleDelta <= totalDelta) {
            metrics.cpuUtilizationPercent =
                100.0 * (totalDelta - idleDelta) / totalDelta;
        }
    }

    previousIdle = idle;
    previousKernel = kernel;
    previousUser = user;
    hasPreviousCpuSample = true;

    MEMORYSTATUSEX memoryStatus;
    memoryStatus.dwLength = sizeof(memoryStatus);

    if (!GlobalMemoryStatusEx(&memoryStatus)) {
        std::cerr << "Error: Could not read Windows memory status.\n";
        return false;
    }

    metrics.memoryUtilizationPercent =
        static_cast<double>(memoryStatus.dwMemoryLoad);

    const unsigned long long bytesPerMB = 1024ULL * 1024ULL;

    metrics.totalMemoryMB = memoryStatus.ullTotalPhys / bytesPerMB;
    metrics.availableMemoryMB = memoryStatus.ullAvailPhys / bytesPerMB;
    metrics.usedMemoryMB =
        (memoryStatus.ullTotalPhys - memoryStatus.ullAvailPhys) / bytesPerMB;

    metrics.totalProcesses = countProcesses();
    metrics.timestamp = currentTimestamp();

    return true;
}

bool appendMetrics(const std::string& outputPath,
                   const SystemMetrics& metrics) {
    std::ifstream existing(outputPath.c_str());
    bool needsHeader = !existing.good() || existing.peek() == std::ifstream::traits_type::eof();
    existing.close();

    std::ofstream output(outputPath.c_str(), std::ios::app);
    if (!output.is_open()) {
        std::cerr << "Error: Cannot open output file: " << outputPath << "\n";
        std::cerr << "Make sure the results/monitoring directory exists.\n";
        return false;
    }

    if (needsHeader) {
        output << "timestamp,data_source,cpu_utilization_percent,"
               << "memory_utilization_percent,total_memory_mb,"
               << "used_memory_mb,available_memory_mb,total_processes\n";
    }

    output << '"' << metrics.timestamp << '"' << ",windows_native_api,"
           << std::fixed << std::setprecision(2)
           << metrics.cpuUtilizationPercent << ','
           << metrics.memoryUtilizationPercent << ','
           << metrics.totalMemoryMB << ','
           << metrics.usedMemoryMB << ','
           << metrics.availableMemoryMB << ','
           << metrics.totalProcesses << '\n';

    return output.good();
}

}  // namespace

int main(int argc, char* argv[]) {
    int sampleCount = 5;
    int intervalMs = 1000;
    std::string outputPath = "results/monitoring/system_metrics.csv";

    if (argc > 1) {
        sampleCount = std::atoi(argv[1]);
    }

    if (argc > 2) {
        intervalMs = std::atoi(argv[2]);
    }

    if (argc > 3) {
        outputPath = argv[3];
    }

    if (sampleCount < 1 || sampleCount > 10000 ||
        intervalMs < 250 || intervalMs > 3600000) {
        std::cerr << "Usage: system_monitor.exe [samples 1-10000] "
                  << "[interval_ms 250-3600000] [output_csv_path]\n";
        return 1;
    }

    std::cout << "NeuroOS System Monitor\n";
    std::cout << "Samples: " << sampleCount
              << ", interval: " << intervalMs << " ms\n";
    std::cout << "Output: " << outputPath << "\n\n";

    unsigned long long previousIdle = 0;
    unsigned long long previousKernel = 0;
    unsigned long long previousUser = 0;
    bool hasPreviousCpuSample = false;

    for (int i = 0; i < sampleCount; ++i) {
        SystemMetrics metrics;

        if (!collectMetrics(metrics, previousIdle, previousKernel,
                           previousUser, hasPreviousCpuSample)) {
            return 1;
        }

        // The first CPU sample establishes a baseline; its CPU value is 0.
        if (!appendMetrics(outputPath, metrics)) {
            return 1;
        }

        std::cout << "[" << (i + 1) << "/" << sampleCount << "] "
                  << metrics.timestamp
                  << " | CPU: " << std::fixed << std::setprecision(2)
                  << metrics.cpuUtilizationPercent << "%"
                  << " | RAM: " << metrics.memoryUtilizationPercent << "%"
                  << " | Processes: " << metrics.totalProcesses << "\n";

        if (i + 1 < sampleCount) {
            Sleep(static_cast<DWORD>(intervalMs));
        }
    }

    std::cout << "\nMonitoring complete. Measurements appended to CSV.\n";
    return 0;
}