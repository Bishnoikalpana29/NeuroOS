#include "scheduler.h" 
#include <algorithm> 
#include <iomanip> 
#include <iostream> 
#include <limits> 
#include <queue> 

namespace { 
    struct InternalProcess 
    { 
        Process process; 
        int remainingTime; 
        int firstStartTime; 
        int completionTime; 
        bool started; 
        bool completed; 
    }; 
    ScheduleResult createResult( 
        const std::string& algorithm, 
        const std::vector<ScheduleEntry>& gantt, 
        const std::vector<InternalProcess>& data 
    ) 
    { 
        ScheduleResult result; 
        result.algorithm = algorithm; 
        result.ganttChart = gantt; 
        double totalTurnaround = 0.0; 
        double totalWaiting = 0.0; 
        double totalResponse = 0.0; 
        
        for (const auto& item : data) { 
            ProcessResult processResult;

            processResult.pid = item.process.pid; 

            processResult.completionTime = item.completionTime;

            processResult.turnaroundTime = item.completionTime - item.process.arrivalTime;

            processResult.waitingTime = processResult.turnaroundTime - item.process.burstTime; 

            processResult.responseTime = item.firstStartTime - item.process.arrivalTime; 

            result.results.push_back(processResult); 

            totalTurnaround += processResult.turnaroundTime; 

            totalWaiting += processResult.waitingTime; 

            totalResponse += processResult.responseTime; 

        } 
        if (!data.empty()) { 
            result.averageTurnaroundTime = totalTurnaround / data.size(); 
            
            result.averageWaitingTime = totalWaiting / data.size(); 
            
            result.averageResponseTime = totalResponse / data.size(); 
        } else { 
            result.averageTurnaroundTime = 0.0; 
            
            result.averageWaitingTime = 0.0; 
            
            result.averageResponseTime = 0.0; 
        } 
        return result; 
    } 
    bool compareArrival( 
        const InternalProcess& a, 
        const InternalProcess& b 
    ) 
    { 
        if (a.process.arrivalTime != b.process.arrivalTime) { 
            return a.process.arrivalTime < b.process.arrivalTime; 
        } return a.process.pid < b.process.pid;
    } 
    } 
    ScheduleResult fcfs(std::vector<Process> processes) { 
        std::vector<InternalProcess> data; 
        
        for (const auto& process : processes) { 
            InternalProcess item; 
            item.process = process; 
            item.remainingTime = process.burstTime; 
            item.firstStartTime = -1; 
            item.completionTime = 0; 
            item.started = false; 
            item.completed = false; 
            data.push_back(item); 
        } 
        std::sort(data.begin(), data.end(), compareArrival); 
        std::vector<ScheduleEntry> gantt; 
        int currentTime = 0; 
        
        for (auto& item : data) { 
            if (currentTime < item.process.arrivalTime) { 
                currentTime = item.process.arrivalTime; 
            } 
            item.firstStartTime = currentTime; 

            item.started = true; 

            int startTime = currentTime; 

            currentTime += item.process.burstTime; 

            item.remainingTime = 0; 

            item.completionTime = currentTime;

            item.completed = true; 

            ScheduleEntry entry; 
            
            entry.pid = item.process.pid; 
            
            entry.startTime = startTime; 
            
            entry.endTime = currentTime; 
            
            gantt.push_back(entry); 
        } 
        return createResult( "FCFS", gantt, data );
    } 
    ScheduleResult sjf(std::vector<Process> processes) {
         std::vector<InternalProcess> data; 
         
         for (const auto& process : processes) {
             InternalProcess item; item.process = process; 
             
             item.remainingTime = process.burstTime; 
             
             item.firstStartTime = -1; 
             
             item.completionTime = 0; 
             
             item.started = false; 
             
             item.completed = false; 
             
             data.push_back(item); 
            }
            std::vector<ScheduleEntry> gantt; 
            
            int currentTime = 0; 
            
            int completedCount = 0; 
            
            int totalProcesses = static_cast<int>(data.size()); 
            
            while (completedCount < totalProcesses) { 
                int selected = -1; 
                
                for (int i = 0; i < totalProcesses; ++i) { 
                    if (data[i].completed) { 
                        continue; 
                    } 
                    if (data[i].process.arrivalTime > currentTime) { 
                        continue; 
                    } 
                    if (selected == -1) { 
                        selected = i; 
                    } 
                    else if ( data[i].process.burstTime < data[selected].process.burstTime ) { 
                        selected = i; 
                    } 
                    else if ( data[i].process.burstTime == data[selected].process.burstTime ) { 
                        if ( data[i].process.arrivalTime < data[selected].process.arrivalTime ) {
                            selected = i; 
                        } 
                        else if ( data[i].process.arrivalTime == data[selected].process.arrivalTime && data[i].process.pid < data[selected].process.pid ) { 
                            selected = i; 
                        } 
                    } 
                } 
                if (selected == -1) { 
                    int nextArrival = std::numeric_limits<int>::max(); 
                    
                    for (const auto& item : data) { 
                        if (!item.completed) { nextArrival = std::min( nextArrival, item.process.arrivalTime ); 
                        } 
                    } 
                    currentTime = nextArrival; continue; 
                } 
                auto& item = data[selected]; 
                
                item.firstStartTime = currentTime; 

                item.started = true; 
                
                int startTime = currentTime; 
                
                currentTime += item.process.burstTime; 
                
                item.remainingTime = 0; 
                
                item.completionTime = currentTime; 
                
                item.completed = true; 
                
                ++completedCount; 
                
                ScheduleEntry entry; 
                
                entry.pid = item.process.pid; 
                
                entry.startTime = startTime; 
                
                entry.endTime = currentTime; 
                
                gantt.push_back(entry); 
            } 
            return createResult( "SJF", gantt, data ); 
        } 
        
        ScheduleResult priorityScheduling( std::vector<Process> processes ) { 
            std::vector<InternalProcess> data; 
            
            for (const auto& process : processes) { 
                InternalProcess item; 
                
                item.process = process; 
                
                item.remainingTime = process.burstTime; 
                
                item.firstStartTime = -1; 
                
                item.completionTime = 0; 
                
                item.started = false; 
                
                item.completed = false; 
                
                data.push_back(item); 
            } 
            std::vector<ScheduleEntry> gantt; 
            
            int currentTime = 0; 
            
            int completedCount = 0; 
            
            int totalProcesses = static_cast<int>(data.size()); 
            
            while (completedCount < totalProcesses) { 
                int selected = -1; 
                for (int i = 0; i < totalProcesses; ++i) { 
                    if (data[i].completed) { 
                        continue;
                    } 
                    if (data[i].process.arrivalTime > currentTime) { 
                        continue; 
                    } 
                    if (selected == -1) { 
                        selected = i; 
                    } 
                    else if ( data[i].process.priority < data[selected].process.priority ) { 
                        selected = i; 
                    }
                    else if ( data[i].process.priority == data[selected].process.priority ) { 
                        if ( data[i].process.arrivalTime < data[selected].process.arrivalTime ) { 
                            selected = i; 
                        } 
                        else if ( data[i].process.arrivalTime == data[selected].process.arrivalTime && data[i].process.pid < data[selected].process.pid ) { 
                            selected = i; 
                        } 
                    } 
                } 
                if (selected == -1) { 
                    int nextArrival = std::numeric_limits<int>::max(); 
                    
                    for (const auto& item : data) { 
                        if (!item.completed) { 
                            nextArrival = std::min( nextArrival,item.process.arrivalTime ); 
                        } 
                    } 
                        
                    currentTime = nextArrival; 
                    continue; 
                } 
                auto& item = data[selected]; 
                item.firstStartTime = currentTime;

                item.started = true; 

                int startTime = currentTime; 

                currentTime += item.process.burstTime;

                item.remainingTime = 0; 

                item.completionTime = currentTime; 

                item.completed = true; 

                ++completedCount; 
                
                ScheduleEntry entry; 
                
                entry.pid = item.process.pid; 
                
                entry.startTime = startTime; 
                
                entry.endTime = currentTime; 
                
                gantt.push_back(entry); 
            } 
            return createResult( "Priority Scheduling", gantt, data ); 
        } 
        ScheduleResult roundRobin( std::vector<Process> processes, int quantum ) { 
            std::vector<InternalProcess> data; 
            for (const auto& process : processes) { 
                InternalProcess item; 
                
                item.process = process; 
                
                item.remainingTime = process.burstTime; 
                
                item.firstStartTime = -1; 
                
                item.completionTime = 0; 
                
                item.started = false; 
                
                item.completed = false; 
                
                data.push_back(item); 
            } 
            std::sort(data.begin(), data.end(), compareArrival); 
            
            std::vector<ScheduleEntry> gantt; 
            
            if (quantum <= 0 || data.empty()) { 
                return createResult( "Round Robin", gantt, data ); 
            } 
            std::queue<int> readyQueue; 
            
            int currentTime = 0; 
            
            int nextProcess = 0; 
            
            int completedCount = 0; 
            
            int totalProcesses = static_cast<int>(data.size()); 
            
            while (completedCount < totalProcesses) { 
                while ( nextProcess < totalProcesses && data[nextProcess].process.arrivalTime <= currentTime ) { 
                    readyQueue.push(nextProcess); 
                    
                    ++nextProcess; 
                } 
                if (readyQueue.empty()) { 
                    
                if (nextProcess < totalProcesses) { 
                    currentTime = data[nextProcess].process.arrivalTime; 
                    continue; 
                } 
            } 
            int index = readyQueue.front(); 
            
            readyQueue.pop(); 
            
            auto& item = data[index]; 
            
            if (!item.started) { 
                item.firstStartTime = currentTime; 
                
                item.started = true; 
            } 
            int startTime = currentTime; 
            
            int executionTime = std::min( quantum, item.remainingTime ); 
            
            currentTime += executionTime; 
            
            item.remainingTime -= executionTime; 
            
            ScheduleEntry entry; 
            
            entry.pid = item.process.pid; 
            
            entry.startTime = startTime; 
            
            entry.endTime = currentTime; 
            
            gantt.push_back(entry); 
            
            while ( nextProcess < totalProcesses && data[nextProcess].process.arrivalTime <= currentTime ) { 
                readyQueue.push(nextProcess); 
                
                ++nextProcess; 
            } 
            if (item.remainingTime > 0) { 
                readyQueue.push(index); 
            } 
            else { 
                item.completed = true; 
                item.completionTime = currentTime; 
                ++completedCount; 
            } 
        } 
        return createResult( "Round Robin", gantt, data ); 
    } 
    
    void printSchedule(const ScheduleResult& result) { 
        std::cout << "\n========================================\n"; 
        std::cout << result.algorithm << "\n"; 
        std::cout << "========================================\n"; 
        std::cout << "\nGantt Chart:\n"; 
        
        for (const auto& entry : result.ganttChart) { 
            std::cout << "[P" << entry.pid << ": " << entry.startTime << "-" << entry.endTime << "] "; 
        } 
        
        std::cout << "\n\n";
        std::cout << std::left 
                  << std::setw(8)
                  << "PID" 
                  << std::setw(15) 
                  << "Completion" 
                  << std::setw(15) 
                  << "Turnaround" 
                  << std::setw(12)
                  << "Waiting" 
                  << std::setw(12) 
                  << "Response" 
                  << "\n"; 
                  
                  std::cout << "------------------------------------------------------------\n"; 
                  
                  for (const auto& item : result.results) { 
                    std::cout 
                        << std::left 
                        << std::setw(8) 
                        << item.pid 
                        << std::setw(15) 
                        << item.completionTime 
                        << std::setw(15) 
                        << item.turnaroundTime
                         << std::setw(12) 
                         << item.waitingTime 
                         << std::setw(12) 
                         << item.responseTime 
                         << "\n"; 
                  } 
                  std::cout 
                         << std::fixed 
                         << std::setprecision(2); 
                         
                         std::cout 
                         << "\nAverage Turnaround Time: " 
                         << result.averageTurnaroundTime 
                         << "\n"; 
                         
                         std::cout 
                         << "Average Waiting Time: " 
                         << result.averageWaitingTime 
                         << "\n"; 
                         
                         std::cout 
                         << "Average Response Time: " 
                         << result.averageResponseTime 
                         << "\n"; 
    }